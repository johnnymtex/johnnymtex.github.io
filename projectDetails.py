import os
import matplotlib.pyplot as plt
from dataload import EUProjectData
import numpy as np

if __name__ == "__main__":
    data = EUProjectData()
    df = data.table_from_query(
    '''select id,acronym,status,title,startDate,endDate, totalCost,ecMaxContribution
        FROM project
        WHERE status != "Terminated"
        order by ecMaxContribution DESC
    ''')

    

    print(df.head())
    
    print("largest project is EUROfusion")

    
    print(df["ecMaxContribution"].mean(),df["ecMaxContribution"].max(),df["ecMaxContribution"].min(),)
    
    plt.title("distribution of project ecMaxContributions")
    plt.hist(df["ecMaxContribution"],bins=100)
    plt.xlabel("max contribution in euros")
    plt.ylabel("count of projects")
    plt.yscale("log")
    plt.savefig(os.path.join("graphs","distribution_of_ecMaxContribution"))
    plt.clf()

    df = data.table_from_query(
    '''select id,acronym,status,title,startDate,endDate, totalCost,ecMaxContribution/(julianday(endDate)-julianday(startDate)) as "dailyContibution"
        FROM project
        WHERE status != "Terminated" AND startDate NOT NULL AND endDate NOT NULL
        order by ecMaxContribution DESC 
    ''')
    print(df.head())
    print("largest is still euro fusion")

    plt.title("distribution of project dailyMaxContribution")
    plt.hist(df["dailyContibution"],bins=100)
    plt.xlabel("max contribution daily in euros")
    plt.ylabel("count of projects")
    plt.yscale("log")
    plt.savefig(os.path.join("graphs","distribution_of_dailyContibution"))
    plt.clf()


    df = data.table_from_query(
    '''select id,acronym,status,title,startDate,endDate,julianday(endDate)-julianday(startDate) as "lengthDays", totalCost,ecMaxContribution
        FROM project
        WHERE status != "TERMINATED" AND startDate NOT NULL AND endDate NOT NULL
        order by lengthDays DESC
    ''')
    print(df.head())
    print("longest projects are the clean sky proposals")

    plt.title("distribution of project length")
    plt.hist(df["lengthDays"],bins=100)
    plt.xlabel("project lengthDays include projections")
    plt.ylabel("count of projects")
    plt.yscale("log")
    plt.savefig(os.path.join("graphs","distribution_of_lengthDays"))
    plt.clf()



    df = data.table_from_query(
        '''SELECT *,totalCost/lengthDays as dailyCost,ecMaxContribution/lengthDays as dailyContibution
            FROM(SELECT id,acronym,status,title,startDate,endDate,julianday(endDate)-julianday(startDate) as "lengthDays", totalCost,ecMaxContribution
            FROM project
            WHERE status = "CLOSED")
            ORDER BY totalCost DESC
        ''')
    
    print(df.head())
    print("of completed projects the air plane project seem to be the most costly")

    plt.title("distribution of totalcosts")
    plt.hist(df["totalCost"],bins=100)
    plt.xlabel("project totalCost only completed projects")
    plt.ylabel("count of projects")
    plt.yscale("log")
    plt.savefig(os.path.join("graphs","distribution_of_totalCost_completed"))
    plt.clf()

    df.sort_values("dailyCost",ascending=False,inplace=True)

    print(df.head())
    print("daily cost is more shifted to technology might have more investments/quicker turnaround")

    plt.title("distribution of dailyCost")
    plt.hist(df["dailyCost"],bins=100)
    plt.xlabel("project dailyCost only completed projects")
    plt.ylabel("count of projects")
    plt.yscale("log")
    plt.savefig(os.path.join("graphs","distribution_of_dailyCost_completed"))
    plt.clf()


    df.sort_values("ecMaxContribution",ascending=False,inplace=True)
    print(df.head())