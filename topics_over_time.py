import matplotlib.pyplot as plt
import os
import pandas as pd


from dataload import EUProjectData
query = '''
SELECT TIME_PERIODS.period,TIME_PERIODS.start_date,TIME_PERIODS.end_date,contribution,topic
FROM TIME_PERIODS
LEFT JOIN
(SELECT period,sum(contribution) AS contribution,"all" AS topic
FROM monthly_group_funding_cache
GROUP BY period

UNION
SELECT period,sum(contribution) AS contribution,"energy and fuels" AS topic
FROM monthly_group_funding_cache
WHERE path2 = "energy and fuels"
GROUP BY period

	UNION
	SELECT period,sum(contribution) as contribution,"renewable energy" AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "renewable energy"
	GROUP BY period
	
UNION
SELECT period,sum(contribution) as contribution,"electronic engineering" AS topic
FROM monthly_group_funding_cache
WHERE path2 = "electronic engineering"
GROUP BY period

UNION
SELECT period,sum(contribution) as contribution,"pharmacology and pharmacy" AS topic
FROM monthly_group_funding_cache
WHERE path2 = "pharmacology and pharmacy"
GROUP BY period


UNION
SELECT period,sum(contribution) as contribution,"optics" AS topic
FROM monthly_group_funding_cache
WHERE path2 = "optics"
GROUP BY period

UNION
SELECT period,sum(contribution) as contribution,"ecology" AS topic
FROM monthly_group_funding_cache
WHERE path2 = "ecology"
GROUP BY period



UNION
SELECT period,sum(contribution) as contribution,"vehicle engineering" AS topic
FROM monthly_group_funding_cache
WHERE path2 = "vehicle engineering"
GROUP BY period
	UNION
	SELECT period,sum(contribution) as contribution,"aerospace engineering" AS topic
	FROM monthly_group_funding_cache
	WHERE path3 = "aerospace engineering"
	GROUP BY period
	
UNION	
SELECT period,sum(contribution) as contribution,"RNA viruses" AS topic
FROM monthly_group_funding_cache
WHERE path3 = "RNA viruses"
GROUP BY period

UNION
SELECT period,sum(contribution) as contribution,"proteins" AS topic
FROM monthly_group_funding_cache
WHERE path4 = "proteins"
GROUP BY period) as topic_funding
ON TIME_PERIODS.period = topic_funding.period
ORDER BY TIME_PERIODS.period
'''



if __name__ == "__main__":

    data = EUProjectData()
    df = data.table_from_query(query)
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["end_date"] = pd.to_datetime(df["end_date"])
    max_period = df["period"].max()
    df = df.set_index("period")
    topics = list(filter(lambda x:x,set(df["topic"])))

    
    

    end_df = pd.DataFrame()
    end_df["period"] = range(max_period+1)
    end_df = end_df.set_index("period")

    end_df = pd.merge(end_df,df.loc[df["topic"] == "all"]["start_date"],how="inner",right_index=True,left_index=True)

    for topic in topics:
        topic_funding = df.loc[df["topic"] == topic]["contribution"]
        topic_funding = topic_funding.rename(topic)

        end_df = pd.merge(end_df,topic_funding,how="left",right_index=True,left_index=True)

    end_df = end_df.fillna(0)


    topics_no_all = list(filter(lambda x:x != "all",topics))

    for topic in topics_no_all:
        end_df[topic] = end_df[topic]/end_df["all"]
    end_df = end_df.fillna(0)
    print(end_df.head())

    plt.title("energy funding")
    plt.plot(end_df["start_date"],end_df["energy and fuels"],label = "energy and fuels")
    plt.plot(end_df["start_date"],end_df["renewable energy"],label = "renewable energy")
    plt.legend()
    plt.savefig(os.path.join("graphs","funding_energy"))
    plt.clf()

    plt.title("planes")
    plt.plot(end_df["start_date"],end_df["vehicle engineering"],label = "vehicle engineering")
    plt.plot(end_df["start_date"],end_df["aerospace engineering"],label = "aerospace engineering")
    plt.legend()
    plt.savefig(os.path.join("graphs","planes"))
    plt.clf()

    plt.title("optics")
    plt.plot(end_df["start_date"],end_df["optics"],label = "optics")
    plt.legend()
    plt.savefig(os.path.join("graphs","optics"))
    plt.clf()

    plt.title("ecology")
    plt.plot(end_df["start_date"],end_df["ecology"],label = "ecology")
    plt.legend()
    plt.savefig(os.path.join("graphs","ecology"))
    plt.clf()

    plt.title("RNA viruses")
    plt.plot(end_df["start_date"],end_df["RNA viruses"],label = "RNA viruses")
    plt.legend()
    plt.savefig(os.path.join("graphs","RNA_viruses"))
    plt.clf()


    plt.title("topic funding groups")
    for topic in topics_no_all:
        plt.plot(end_df["start_date"],end_df[topic],label = topic)
    plt.xlabel("time")
    plt.xlabel("percent of total")
    plt.legend()
    plt.savefig(os.path.join("graphs","funding_groups"))
    plt.clf()

    plt.title("pharmacology and pharmacy")
    plt.plot(end_df["start_date"],end_df["pharmacology and pharmacy"],label = "pharmacology and pharmacy")
    plt.xlabel("time")
    plt.xlabel("percent of total")
    plt.legend()
    plt.savefig(os.path.join("graphs","pharmacology_and_pharmacy"))
    plt.clf()

    

    all_topic = df.loc[df["topic"] == "all"]
    plt.title("all eu ec funding")
    plt.xlabel("funding period")
    plt.ylabel("funding amount")
    plt.plot( all_topic["start_date"],all_topic["contribution"])
    plt.savefig(os.path.join("graphs","all_funding"))
    plt.clf()