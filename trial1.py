from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import sys
import bson
client = MongoClient('mongodb+srv://harshseth09:messis@cluster0.hfphg.mongodb.net/options?retryWrites=true&w=majority')
db = client['NIFTYoptions']
col=db['05-Aug-2021_ce']
query={'strikePrice':16300}
x=col.find(query)
lst=[]
for i in x:
    lst.append(i)
df=pd.DataFrame(lst)
print(df[0])
# dates=[]
# for i in df['date']:
#     dates.append(i.date())
# df['just_date']=dates
# for i,row in df.iterrows():
#     if(str(row['just_date'])!='2021-08-04'):
#         df.drop(i,inplace=True)
# plt.plot(df['date'],df['openInterest'])
# plt.show()

def filter_by_date(date,frame):
    dates=[]
    for i in frame['date']:
        dates.append(i.date())
    frame['just_date']=dates
    for i,row in frame.iterrows():
        if str(row['just_date'])!=date:
            frame.drop(i,inplace=True)
    print(frame)
#filter_by_date('2021-08-04',df)
