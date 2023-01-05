import matplotlib.pyplot as plt
import os
import pandas as pd
from dataload import EUProjectData
import string
import numpy as np
import json

project_query = '''
SELECT project.id,project.acronym,project.title,startDate,endDate,objective,webLink.physUrl
FROM project
INNER JOIN 
(SELECT DISTINCT projectID
FROM euroSciVoc
WHERE path2 in ("energy and fuels")) as esv
ON project.id =esv.projectID
LEFT OUTER JOIN webLink ON project.id = webLink.projectID
where type = "relatedWebsite" 
'''

country_energy_funding_query = '''
SELECT country,power_type,sum(funding) as "funding"
FROM
(SELECT organization.country,
CASE
	WHEN path4 is null THEN path3
	ELSE path4
END as "power_type",
CASE 
	WHEN ecContribution is null THEN netEcContribution
	WHEN netEcContribution is null THEN ecContribution
	ELSE max(ecContribution,netEcContribution)
END as "funding"
FROM organization
INNER JOIN euroSciVoc ON organization.projectID = euroSciVoc.projectID
WHERE euroSciVoc.path3 in ("fossil energy","nuclear energy","biofuels") OR path4 in ("geothermal energy","hydroelectricity","wind power","solar energy") AND not (ecContribution is null AND netEcContribution is null))
GROUP BY country,power_type
'''

funding_query = '''
SELECT TIME_PERIODS.period,TIME_PERIODS.start_date,TIME_PERIODS.end_date,contribution,topic
FROM TIME_PERIODS
LEFT JOIN

(
SELECT period,sum(contribution) AS contribution,"all" AS topic
FROM monthly_group_funding_cache
GROUP BY period

UNION
SELECT period,sum(contribution) AS contribution,path2 AS topic
FROM monthly_group_funding_cache
WHERE path2 = "energy and fuels"
GROUP BY period



	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "fossil energy"
	GROUP BY period


	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "nuclear energy"
	GROUP BY period
	
	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "renewable energy"
	GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "geothermal energy"
		GROUP BY period
		
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "hydroelectricity"
		GROUP BY period
			
		
		
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "solar energy"
		GROUP BY period
			
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "wind power"
		GROUP BY period
	UNION


    SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "biofuels"
	GROUP BY period


		
) as topic_funding
ON TIME_PERIODS.period = topic_funding.period
ORDER BY TIME_PERIODS.period
'''
grouping_table = {
    "all":None,
    "energy and fuels":{
        "fossil energy":None,
        "nuclear energy":None,
        "renewable energy":{
            "geothermal energy":None,
            "hydroelectricity":None,
            "solar energy":None,
            "wind power":None
        },
        "biofuels":None
    }
}

if __name__ == "__main__":
    print("generating final data")

    data = EUProjectData()

    funding_instance_table = data.table_from_query(funding_query)
    
    funding_instance_table["start_date"] = pd.to_datetime(funding_instance_table["start_date"])
    funding_instance_table["end_date"] = pd.to_datetime(funding_instance_table["end_date"])
    funding_instance_table["contribution"] = funding_instance_table["contribution"].fillna(0)

    funding_table = pd.DataFrame()
    funding_table["period"] = range(funding_instance_table["period"].max()+1)
    funding_table = funding_table.set_index("period")
    funding_instance_table = funding_instance_table.set_index("period")
    funding_table = pd.merge(funding_table,funding_instance_table.loc[funding_instance_table["topic"] == "all"]["start_date"],how="inner",right_index=True,left_index=True)

    topics = list(filter(lambda x:x,set(funding_instance_table["topic"])))
    for topic in topics:
        topic_funding = funding_instance_table.loc[funding_instance_table["topic"] == topic]["contribution"]
        topic_funding = topic_funding.rename(topic)

        funding_table = pd.merge(funding_table,topic_funding,how="left",right_index=True,left_index=True)
    funding_table = funding_table.fillna(0)

    funding_table["all"] = 0
    for topic in topics:
        funding_table["all"] = funding_table["all"] + funding_table[topic]



    with open("topic_grouping.json",'w') as f:
        json.dump({"energy and fuels":grouping_table["energy and fuels"]},f)
    
    collect_keys = ["energy and fuels",grouping_table["energy and fuels"]]
    index = 0
    while(index < len(collect_keys)):
        if(isinstance(collect_keys[index],str)):
            index = index + 1
        elif(isinstance(collect_keys[index],type(None))):
            del collect_keys[index]
        else:
            collect_keys = collect_keys + list(collect_keys[index].keys()) + list(collect_keys[index].values())
            del collect_keys[index]


	


    funding_table[collect_keys + ["start_date"]].to_json("funding_data.json",orient="records")

    projects = data.table_from_query(project_query)
    new_events = pd.read_excel("DataVis_GraphDataPoints.xlsx")

    projects["Date"] = pd.to_datetime((pd.to_datetime(projects["startDate"]).values.astype(np.int64)+pd.to_datetime(projects["endDate"]).values.astype(np.int64))/2)
    projects["Notes"] = projects["objective"]
    projects["Name"] = projects["title"]
    projects["Acronym"] = projects["acronym"]
    projects["Link"] = projects["physUrl"]
    projects["Type"] = "projects" 

    new_events["Type"] = "news"
    new_events["Date"] = pd.to_datetime(new_events["Date"])
    new_events["Acronym"] = new_events["Name"]

    all_events = pd.concat([projects[["Date","Type","Acronym","Name","Notes","Link"]],new_events[["Date","Type","Acronym","Name","Notes","Link"]]])
    all_events.to_json("event_data.json",orient="records")


    code_to_name = {
        "TOTAL":"total",
        
        "C0000X0350-0370":"fossil energy",#solid fossil fuels
        "C0350-0370":"fossil energy",#manufactured gasses
        "P1000":"fossil energy", #peat
        "S2000":"fossil energy",#oil shale
        "G3000":"fossil energy", #natural gas
        
        "O4000XBIO":"fossil energy", # oil and petro - bio

        "RA100":"hydroelectricity", #hydro
        "RA200":"geothermal energy", #geothermal
        "RA300":"wind power", #wind
        "RA410":"solar energy", #solar thermal
        "RA420":"solar energy", #solar photovoltaic
        "RA500":"hydroelectricity", #tidal and wave
        "R5110-5150_W6000RI":"biofuels", # primary solid bio fules
        "R5210P":"biofuels", #bio gasoline
        "R5220P":"biofuels", #bio diesels
        "R5290":"biofuels",#other liquid bio
        "R5300":"biofuels",#bio gas
        "W6100_6220":None,#non renewable waste
        "W6210":None,#renewable waste
        "N900H":"nuclear energy" #nuclear heat
        

    }
    consumption_data = pd.read_csv("consumption.csv")[["siec","geo","TIME_PERIOD","OBS_VALUE"]]
    consumption_data["power_type"] =consumption_data["siec"].apply(lambda x:code_to_name[x]) 
    consumption_data["country"] = consumption_data["geo"]

    consumption_data= consumption_data.drop("geo",axis=1)
    consumption_data = consumption_data.loc[~pd.isnull(consumption_data["power_type"])]
    consumption_data = consumption_data.drop("siec",axis=1)

    consumption_data = consumption_data.loc[consumption_data["TIME_PERIOD"]==2020]
    consumption_data = consumption_data.groupby(["country","power_type"]).sum()[["OBS_VALUE"]]
    consumption_data["usage"] = consumption_data["OBS_VALUE"]
    consumption_data = consumption_data.drop("OBS_VALUE",axis=1).reset_index()
    consumption_data = consumption_data.loc[consumption_data["country"] != "EU27_2020"]

    country_energy_funding_df = data.table_from_query(country_energy_funding_query)
    print(set(consumption_data["country"]))
    country_energy_funding_df = country_energy_funding_df.reset_index().drop("index",axis=1)
    country_energy_funding_df = country_energy_funding_df.loc[country_energy_funding_df["country"].isin(set(consumption_data["country"]))]
    total_section = country_energy_funding_df[["country","funding"]].groupby(["country"]).sum().reset_index()
    total_section["power_type"] = "total"
    country_energy_funding_df = pd.concat([country_energy_funding_df,total_section])

    joined = pd.merge(consumption_data,country_energy_funding_df,how="outer",on = ["power_type","country"])
    total_group = joined.loc[joined["power_type"] == "total"].copy()
    total_group["total_usage"] = total_group["usage"]
    total_group["total_funding"] = total_group["funding"]
    total_group = total_group.drop(["power_type","usage","funding"],axis = 1)

    joined = pd.merge(joined,total_group,on = ["country"])

    joined = joined.fillna(0)


    joined.to_json("country_consumption_funding_data.json",orient="records")


    greenhouse_emissions_df = pd.read_csv("greenhouse_emissions.csv")
    greenhouse_emissions_df = greenhouse_emissions_df.loc[greenhouse_emissions_df["unit"] == "I90"].loc[greenhouse_emissions_df["geo"] == "EU27_2020"]
    greenhouse_emissions_df = greenhouse_emissions_df.loc[greenhouse_emissions_df["src_crf"] == "TOTX4_MEMONIA"].reset_index().drop("index",axis=1)
    print(greenhouse_emissions_df)
    greenhouse_emissions_df = greenhouse_emissions_df[["geo","TIME_PERIOD","OBS_VALUE"]]
    greenhouse_emissions_df = greenhouse_emissions_df.loc[greenhouse_emissions_df["geo"] == "EU27_2020"].reset_index().drop("index",axis=1)

    greenhouse_emissions_df.to_json("greenhouse_emissions.json",orient="records")
    print(greenhouse_emissions_df)





