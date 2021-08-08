from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import sys


def filter_by_date(date,frame):
    dates=[]
    for i in frame['date']:
        dates.append(i.date())
    frame['just_date']=dates
    for i,row in frame.iterrows():
        if str(row['just_date'])!=date:
            frame.drop(i,inplace=True) 
    return frame

def plotting(n,d,s):
    indices=['NIFTY', 'BANKNIFTY']
    expiry_dt_lst=['05-Aug-2021','12-Aug-2021','18-Aug-2021','26-Aug-2021']
    if ((n not in indices) or (d not in expiry_dt_lst)):
        sys.exit('name entered is incorrect')
    else:
        client = MongoClient('mongodb+srv://harshseth09:messis@cluster0.hfphg.mongodb.net/options?retryWrites=true&w=majority')
        db=client[n+'options']
        query={'strikePrice':s}
        plot1 = plt.subplot2grid((7,1),(0,0),rowspan=2,colspan=1)
        plot2 = plt.subplot2grid((7,1),(2,0),rowspan=2,colspan=1)
        for i in ['_ce','_pe']:
            col=db[d+i]
            x=col.find(query)
            lst=[]
            for j in x:
                lst.append(j)
            df=pd.DataFrame(lst)
            time=df['date']
            oi=df['openInterest']
            if i=='_ce':
                plot1.plot(time,oi)
                plot1.set_title('ce')
            else:
                plot2.plot(time,oi)
                plot2.set_title('pe')
        plt.show()


def plot_by_date(n,d,s,entered_date):
    indices=['NIFTY', 'BANKNIFTY']
    expiry_dt_lst=['05-Aug-2021','12-Aug-2021','18-Aug-2021','26-Aug-2021']
    if ((n not in indices) or (d not in expiry_dt_lst)):
        sys.exit('name entered is incorrect')
    else:
        client = MongoClient('mongodb+srv://harshseth09:messis@cluster0.hfphg.mongodb.net/options?retryWrites=true&w=majority')
        db=client[n+'options']
        query={'strikePrice':s}
        plot1 = plt.subplot2grid((7,1),(0,0),rowspan=2,colspan=1)
        plot2 = plt.subplot2grid((7,1),(2,0),rowspan=2,colspan=1)
        for i in ['_ce','_pe']:
            col=db[d+i]
            x=col.find(query)
            lst=[]
            for j in x:
                lst.append(j)
            df=pd.DataFrame(lst)
            df=filter_by_date(entered_date,df)
            time=df['date']
            oi=df['openInterest']
            if i=='_ce':
                plot1.plot(time,oi)
                plot1.set_title('ce')
            else:
                plot2.plot(time,oi)
                plot2.set_title('pe')
        plt.show()

k=int(input('enter 1 for plotting OR 2 for plotting by a specific date'))
if k==1:
    name=input('enter name of incices')
    date=input('enter expiry date in dd-month-yyyy format')
    sp=int(input('enter strike price'))
    plotting(name,date,sp)
elif k==2:
    name=input('enter name of incices')
    date=input('enter expiry date in dd-month-yyyy format')
    sp=int(input('enter strike price'))
    ed=input('enter specific date in yyyy-mm-dd  format')
    plot_by_date(name,date,sp,ed)

