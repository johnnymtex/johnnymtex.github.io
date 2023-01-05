
project_query = '''
SELECT DISTINCT euroSciVoc.projectID,acronym,title,project.status,startDate,endDate,ecMaxContribution,objective,rcn,type,physUrl,path0,path1,path2,path3,path4,path5,
CASE 
	WHEN path5 is not NULL THEN path5
	WHEN path4 is not NULL THEN path4
	WHEN path3 is not NULL THEN path3
	WHEN path2 is not NULL THEN path2
	WHEN path1 is not NULL THEN path1
END as last
FROM euroSciVoc
INNER JOIN project on euroSciVoc.projectID = project.id
INNER JOIN webLink on webLink.projectID = project.id
WHERE path2 in ("ecology","energy and fuels")

'''
grouping_table = {
    "energy and fuels":{
        "energy conversion":None,
        "fossil energy":{
            "coal":None,
            "natural gas":None,
            "petroleum":None,
        },
        "fuel cells":None,
        "liquid fuels":None,
        "nuclear energy":None,

        "renewable energy":{
            "geothermal energy":None,
            "hybrid energy":None,
            "hydroelectricity":{
                "marine energy":None
            },
            "hydrogen energy":None,
            "solar energy":{
                "concentrated solar power":None,
                "photovoltaic":None,
                "solar thermal":None,
            },
            "wind power":None
        },
        "synthetic fuels":None
    },
    "ecology":{
        "ecosystems":{
            "coastal ecosystems":None,
            "freshwater ecosystems":None,

        },
        "evolutionary ecology":None,
        "invasive species":None,
        "landscape ecology":None,
    }
}

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
	WHERE path3 = "energy conversion"
	GROUP BY period

	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "fossil energy"
	GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "coal"
		GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "natural gas"
		GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "petroleum"
		GROUP BY period
	
	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "fuel cells"
	GROUP BY period
	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "liquid fuels"
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
		WHERE path4 = "hybrid energy"
		GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "hydroelectricity"
		GROUP BY period
			UNION
			SELECT period,sum(contribution) AS contribution,path5 AS topic
			FROM monthly_group_funding_cache
			WHERE path5 = "marine energy"
			GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "hydrogen energy"
		GROUP BY period
		
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "solar energy"
		GROUP BY period
			UNION
			SELECT period,sum(contribution) AS contribution,path5 AS topic
			FROM monthly_group_funding_cache
			WHERE path5 = "concentrated solar power"
			GROUP BY period
			UNION
			SELECT period,sum(contribution) AS contribution,path5 AS topic
			FROM monthly_group_funding_cache
			WHERE path5 = "photovoltaic"
			GROUP BY period
			UNION
			SELECT period,sum(contribution) AS contribution,path5 AS topic
			FROM monthly_group_funding_cache
			WHERE path5 = "solar thermal"
			GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "wind power"
		GROUP BY period
	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "synthetic fuels"
	GROUP BY period

	UNION	
SELECT period,sum(contribution) AS contribution,path2 AS topic
FROM monthly_group_funding_cache
WHERE path2 = "ecology"
GROUP BY period
	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "ecosystems"
	GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "coastal ecosystems"
		GROUP BY period
		UNION
		SELECT period,sum(contribution) AS contribution,path4 AS topic
		FROM monthly_group_funding_cache
		WHERE path4 = "freshwater ecosystems"
		GROUP BY period
	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "evolutionary ecology"
	GROUP BY period
	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "invasive species"
	GROUP BY period
	UNION
	SELECT period,sum(contribution) AS contribution,path3 AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "landscape ecology"
	GROUP BY period
		
) as topic_funding
ON TIME_PERIODS.period = topic_funding.period
ORDER BY TIME_PERIODS.period
'''

import matplotlib.pyplot as plt
import os
import pandas as pd
from dataload import EUProjectData
import string
import json

if __name__ == "__main__":
    print("hello world")

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
    
    norm_topics = list(map(lambda x:f"norm {x}",topics))
    for norm_topic,topic in zip(norm_topics,topics):
        funding_table[norm_topic] = funding_table[topic]#/funding_table["all"]

    print(funding_table.head())

    funding_table=funding_table.reset_index()
    for norm_topic,topic in zip(norm_topics,topics):
        if topic != "all":
            plt.plot(funding_table["start_date"],funding_table[norm_topic],label = topic)
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("funding")
    plt.title("funding of all topics")
    plt.savefig(os.path.join("graphs","all_funding_climate_1"))
    plt.clf()


    graph_topics = list(grouping_table.keys()) + ["all"]

    for topic in graph_topics:
        plt.plot(funding_table["start_date"],funding_table[topic],label = topic)
    plt.legend()
    plt.title("top level topics")
    plt.savefig(os.path.join("graphs","top_level_1"))
    plt.clf()

    graph_topics = list(grouping_table["energy and fuels"].keys()) + ["energy and fuels"]

    for topic in graph_topics:
        plt.plot(funding_table["start_date"],funding_table[f"norm {topic}"],label = topic)
    plt.legend()
    plt.title("energy and fuels")
    plt.savefig(os.path.join("graphs","just_energy_and_fuel_1"))
    plt.clf()

    graph_topics = list(grouping_table["energy and fuels"]["renewable energy"].keys()) + ["renewable energy"]

    for topic in graph_topics:
        plt.plot(funding_table["start_date"],funding_table[f"norm {topic}"],label = topic)
    plt.legend()
    plt.title("renewable energy")
    plt.savefig(os.path.join("graphs","renewable_energy_1"))
    plt.clf()

    graph_topics = list(grouping_table["energy and fuels"]["renewable energy"].keys())

    for topic in graph_topics:
        plt.plot(funding_table["start_date"],funding_table[f"norm {topic}"],label = topic)
    plt.legend()
    plt.title("renewable energy additional")
    plt.savefig(os.path.join("graphs","renewable_energy_additional"))
    plt.clf()

    graph_topics = list(grouping_table["ecology"].keys()) + ["ecology"]

    for topic in graph_topics:
        plt.plot(funding_table["start_date"],funding_table[f"norm {topic}"],label = topic)
    plt.legend()
    plt.title("renewable energy")
    plt.savefig(os.path.join("graphs","ecology_1"))
    plt.clf()

    graph_topics = list(grouping_table["energy and fuels"]["renewable energy"]["hydroelectricity"].keys()) + ["hydroelectricity"]

    for topic in graph_topics:
        plt.plot(funding_table["start_date"],funding_table[f"norm {topic}"],label = topic)
    plt.legend()
    plt.title("renewable energy")
    plt.savefig(os.path.join("graphs","hydroelectricity_1"))
    plt.clf()


    project_df = data.table_from_query(project_query)

    all_entries = []
    for project_id in list(set(project_df["projectID"])):

        project = project_df.loc[project_df["projectID"] == project_id]

        project_title = "".join(filter(lambda x:x in string.printable,list(set(project["title"]))[0]))
        project_start = list(set(project["startDate"]))[0]
        project_end = list(set(project["endDate"]))[0]

        project_links = list(set(project["physUrl"]))

        entry = f"{project_title} {project_start}->{project_end}\n" 

        for link in project_links:
            entry += f"\t {link}\n"
        all_entries.append(entry)
    with open("project_info.txt",'w') as f:
        for entry in all_entries:
            f.write(entry)


    with open("topic_grouping.json",'w') as f:
        json.dump({"energy and fuels":grouping_table["energy and fuels"]},f)
    
    collect_keys = ["all","energy and fuels",grouping_table["energy and fuels"]]
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
