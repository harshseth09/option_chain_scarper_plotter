import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from tkinter import *

def onclickindex_button():
	index_name=index.get()
	o_type='_'+ce_pe.get()
	expiry_date=expiry.get()
	print(index_name,o_type,expiry_date)
  
# Creating tkinter window
window = tk.Tk()
window.title('Option plotter')
window.geometry('500x250')
client = MongoClient('mongodb+srv://harshseth09:messis@cluster0.hfphg.mongodb.net/options?retryWrites=true&w=majority')
  
# label text for title
ttk.Label(window, text = "OI/ LTP plotter", 
          background = 'green', foreground ="white", 
          font = ("Times New Roman", 15)).grid(row = 0, column = 1)
  
# label
ttk.Label(window, text = "Select the INDEX :",
          font = ("Times New Roman", 10)).grid(column = 0,
          row = 5, padx = 10, pady = 25)
  
index=['NIFTY','BANKNIFTY']
clicked=StringVar()
clicked.set(1)
drop = OptionMenu( window , clicked , *index )
drop.pack()
#expiry
ttk.Label(window, text = "Enter expirey in dd-mon-yyyy format :",
          font = ("Times New Roman", 10)).grid(column = 0,
          row = 7, padx = 10, pady = 25)
expiry = ttk.Entry(window)
expiry.grid(column=1, row=7)
#ce_pe
ttk.Label(window, text = "Enter option type",
          font = ("Times New Roman", 10)).grid(column = 0,
          row = 9, padx = 10, pady = 25)
ce_pe = ttk.Combobox(window, width = 27, textvariable = n)
ce_pe['values'] = ('ce', 'pe')  
ce_pe.grid(column = 1, row = 9)
ce_pe.current(1)


index_button=Button(window, text='Submit',width=20,bg='brown',fg='white',command=onclickindex_button).grid(column=0,row=11)
window.mainloop()










