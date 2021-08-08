from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import *


def plotting(n,d,s):
    fig=plt.figure()
    ce_plot=fig.add_subplot(131)
    pe_plot=fig.add_subplot(132)
    indices=['NIFTY', 'BANKNIFTY']
    expiry_dt_lst=['05-Aug-2021','12-Aug-2021','18-Aug-2021','26-Aug-2021']
    if ((n not in indices) or (d not in expiry_dt_lst)):
        sys.exit('name entered is incorrect')
    else:
        client = MongoClient('mongodb+srv://harshseth09:messis@cluster0.hfphg.mongodb.net/options?retryWrites=true&w=majority')
        db=client[n+'options']
        query={'strikePrice':s}
        for i in ['_ce','_pe']:
            col=db[d+i]
            x=col.find(query)
            lst=[]
            for j in x:
                lst.append(j)
            df=pd.DataFrame(lst)
            time= df['date']
            oi=df['lastPrice']
            if i=='_ce':
                ce_plot.plot(time,oi)
                ce_plot.title.set_text('CE')
                ce_plot.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom='off',      # ticks along the bottom edge are off
                top='off',         # ticks along the top edge are off
                labelbottom='off'  # labels along the bottom edge are off)
                                    )
                
            else:
                pe_plot.plot(time,oi)
                pe_plot.title.set_text('PE')
        plt.show()
name=input('enter name of indices in CAPITAL ')
date=input('enter expiry date in dd-mon-yyyy format ')
strike_price=int(input('enter strikeprice '))
plotting(name,date,strike_price)