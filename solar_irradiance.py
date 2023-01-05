import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

filename = "data/solarContributions.csv"

df = pd.read_csv(filename, index_col="projectID", sep= ",")

energySources = ["solar energy", "wind power", "nuclear energy", "hydroelectricity", "biofuels", "fossil energy"]
energyDict = {}

df = df[df["path4"].isin(energySources)]

totalMoney = {}

for i in range(len(df["country"].unique())):
    df_copy = df[df["country"] == (df["country"].unique())[i]]
    
    for source in energySources:
        df_copy_copy = df_copy[df_copy["path4"] == source]
        energyDict[source] = sum(df_copy_copy["ecContribution"].tolist())
        print(energyDict[source])
    
    totalMoney[df["country"].unique()[i]] = energyDict

print(totalMoney)

filename = "data/consumption.csv"

dfConsumption = pd.read_csv(filename, sep = ";", decimal = ",", thousands=" ")

countries = list(df["country"].unique())
finalCountries = []
finalMoney = []

for country in countries:
    if country in dfConsumption["Country"].tolist():
        print(country)
        finalCountries.append(country)
        finalMoney.append(totalMoney[country])

""" finalmoney = []

flag = 0

for i in range(len(dfConsumption["Country"])):
    for j in range(len(df["country"].unique())):
        if dfConsumption.loc[i, "Country"] == (df["country"].unique())[j]:
            finalmoney.append(totalMoney[j])
            flag = 1
            break

    if flag == 0:
        finalmoney.append(0)

    flag = 0 """

dfConsumption.drop(0, inplace=True)

dfConsumption["fossilSum"] = dfConsumption["Solid fossil fuels"] + dfConsumption["Manufactured gases"] + dfConsumption["Peat and peat products"] + dfConsumption["Oil shale and oil sands"] + dfConsumption["Natural gas"] + dfConsumption["Oil and petroleum products (excluding biofuel portion)"]
dfConsumption["hydroSum"] = dfConsumption["Hydro"] + dfConsumption["Tide, wave, ocean"]
dfConsumption["geoSum"] = dfConsumption["Geothermal"]
dfConsumption["windSum"] = dfConsumption["Wind"]
dfConsumption["solarSum"] = dfConsumption["Solar thermal"] + dfConsumption["Solar photovoltaic"]
dfConsumption["bioSum"] = dfConsumption["Primary solid biofuels"] + dfConsumption["Pure biogasoline"] + dfConsumption["Pure biodiesels"] + dfConsumption["Other liquid biofuels"] + dfConsumption["Biogases"]
dfConsumption["nuclearSum"] = dfConsumption["Nuclear heat"]

fossilContribution = []
hydroContribution = []
geoContribution = []
windContribution = []
solarContribution = []
bioContribution = []
nuclearContribution = []

print(dfConsumption.head())

""" for df_country in dfConsumption["Country"]:
    for j in range(len(countries)):
        if df_country == countries[j]:
 """
            

""" fig = plt.figure(figsize=(8,6))

x = dfConsumption["ecContribution"]
y = dfConsumption["solarSum"]/dfConsumption["Total"]
labels = []

for i in range(len(dfConsumption["Country"])):
    labels.append(str(dfConsumption.iloc[i]["Country"]))

plt.scatter(x, y)

for i, txt in enumerate(labels):
    plt.annotate(txt, (x.iloc[i], y.iloc[i]))

plt.savefig("graphs/fractionSolar.png")

fig = plt.figure(figsize=(8,6))
y = dfConsumption["solarSum"]

plt.scatter(x, y)

for i, txt in enumerate(labels):
    plt.annotate(txt, (x.iloc[i], y.iloc[i]))

plt.savefig("graphs/absoluteSolar.png") """