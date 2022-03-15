import pandas as pd
import matplotlib.pyplot as plt
PATH="/Users/hannaalbright1/Desktop/CSCI 183/"

def readCSV(iFile, cols):
    print("Reading in File: ", iFile)
    df=pd.read_csv(iFile, header=0, delimiter=",", usecols=cols)
    return df

def plotGraphs(df, target): #scatter and line
    for label in df.drop(target, axis=1).columns:
        if df[label].dtype in ['int64', 'float64']:
            df.boxplot(column=target, by=label)
            name = PATH+target+"/"+label + "graph.png"
            plt.savefig(name)
            plt.close()

sDeaths=readCSV(PATH+"Medical_Examiner-Coroner__Suicide_Deaths_dataset.csv", ["Death Date", "Age", "Race", "Gender"])
sDeaths['Death Date']=pd.to_datetime(sDeaths['Death Date'])
sDeaths.set_index('Death Date', inplace=True)
sDeaths.index=sDeaths.index.normalize()
sDeaths['Race'].replace(['White', 'Hispanic', 'Asian', 'OtherPacificIslander', 'Other','BlackAfricanAmerican', 'Unknown', 'American Indian'], range(0,8), inplace=True)
sDeaths['Gender'].replace(['Male', 'Female', None], [0,1,2], inplace=True)
sDeaths_2020=sDeaths['2020-02':'2021-01-31']
sDeaths_2019=sDeaths['2019-01':'2019-12-31']

sDeaths_2019.to_csv(PATH+"sDeaths2019.csv")
cCases=readCSV(PATH+"COVID-19_case_counts_by_date.csv",["Date", "Total_cases", "New_cases"])
cCases['Date']=pd.to_datetime(cCases['Date'])
cCases.set_index('Date', inplace=True)
c2020=cCases['2020-02':'2021-01-31']#first covid case documented on 2020/1/27 so start at the beginning of the next month
df_2020=sDeaths_2020.join(c2020['Total_cases'], how='left')
df_2020.to_csv(PATH+"sDeaths2020.csv")

df3=df_2020.index.to_frame(index=False)
df_2020["tsuicides_2020"]=df3.index+1
df_2020.to_csv(PATH+"sDeaths2020_count.csv")
df4=sDeaths_2019.index.to_frame(index=False)
sDeaths_2019['tsuicides_2019']=df4.index+1
sDeaths_2019.to_csv(PATH+"sDeaths2019_count.csv")

plotGraphs(sDeaths_2019.drop("Age", axis=1), "tsuicides_2019")
plotGraphs(df_2020.drop(["Age", "Total_cases"], axis=1), "tsuicides_2020")

ax1=df_2020.plot.scatter(y="tsuicides_2020", x="Age", color="b", marker="^", alpha=0.7)
sDeaths_2019.plot.scatter(y="tsuicides_2019", x="Age", color="g", ax=ax1, alpha=0.7)
plt.savefig( PATH +"suicidesAgegraph.png")
plt.close()
df_2020.plot.scatter(y="tsuicides_2020", x="Total_cases", color="b", marker="^", alpha=0.7)
plt.savefig( PATH +"suicidesTotal_casesraph.png")
plt.close()