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

def plotNoTarget(df, df2): #scatter and line
    dfcopy=df.copy()
    for label in df.columns:
        dfcopy.drop(label, axis=1, inplace=True)
        for label2 in dfcopy.columns:
            ax1=df.plot.scatter(y=label2, x=label, color="b", marker="^", alpha=0.7)
            df2.plot.scatter(y=label2, x=label, color="g", ax=ax1, alpha=0.7)
            name = PATH +"_"+label + label2+ "graph.png"
            plt.savefig(name)
            plt.close()

def perMonth(df1, df2):
    df1.drop("Total_cases", axis=1, inplace=True)
    for x in range(1,13):
        amonth1=df1.loc[df1.index.month==x]
        amonth2=df2.loc[df2.index.month == x]
        plotNoTarget(amonth1, amonth2, x)
    #
    # resampler1=df1.resample("M")
    # resampler2 = df2.resample("M")
    # for aMonth in resampler1.groups:
    #     plotNoTarget(resampler1.get_group(aMonth),resampler2.get_group(aMonth),aMonth.month)

sDeaths=readCSV(PATH+"Medical_Examiner-Coroner__Suicide_Deaths_dataset.csv", ["Death Date", "Age", "Race", "Gender"])
sDeaths['Death Date']=pd.to_datetime(sDeaths['Death Date'])
sDeaths.set_index('Death Date', inplace=True)
sDeaths['Race'].replace(['White', 'Hispanic', 'Asian', 'OtherPacificIslander', 'Other','BlackAfricanAmerican', 'Unknown', 'American Indian'], range(0,8), inplace=True)
sDeaths['Gender'].replace(['Male', 'Female', None], [0,1,2], inplace=True)
sDeaths_2020=sDeaths['2020-02':'2021-01-31']
sDeaths_2019=sDeaths['2019-01':'2019-12-31']
print(sDeaths_2020["Age"].size)
print(sDeaths_2019["Age"].size)

sDeaths_2019.to_csv(PATH+"sDeaths2019.csv")
cCases=readCSV(PATH+"COVID-19_case_counts_by_date.csv",["Date", "Total_cases", "New_cases"])
cCases['Date']=pd.to_datetime(cCases['Date'])
cCases.set_index('Date', inplace=True)
c2020=cCases['2020-02':'2021-01-31']#first covid case documented on 2020/1/27 so start at the beginning of the next month
sDeaths.index=sDeaths.index.normalize()
df_2020=sDeaths_2020.join(c2020['Total_cases'], how='left')
df_2020.to_csv(PATH+"sDeaths2020.csv")

df3=df_2020.index.to_frame(index=False)
df_2020["tsuicides_2020"]=df3.index+1
df_2020.to_csv(PATH+"sDeaths2020_count.csv")
#df_2020['count']=df_2020.index
df4=sDeaths_2019.index.to_frame(index=False)
sDeaths_2019['tsuicides_2019']=df4.index+1
sDeaths_2019.to_csv(PATH+"sDeaths2019_count.csv")
#sDeaths_2019['count']=sDeaths_2019.index
#plotNoTarget(df_2020.drop("Total_cases", axis=1),sDeaths_2019)
print(sDeaths_2020["Age"].size)
print(sDeaths_2019["Age"].size)
df_2020['tsuicides_2020'].plot(style='b')
plt.savefig(PATH+"line.png")
plt.close()
sDeaths_2019['tsuicides_2019'].plot(style='g')
plt.savefig(PATH+"line2.png")
plt.close()

# plotGraphs(sDeaths_2019, "tsuicides_2019")
# plotGraphs(df_2020, "tsuicides_2020")
