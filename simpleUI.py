from tkinter import *
from tkinter import messagebox
import reports_generator as rg
import consolidated_lot_report as clr
import sqlite as sq

#Global output list storing the customer IDS the UI iterates through to produce reports
OUTPUT_LIST = [1003151]


class NonExistant(Exception):
    '''Exception made to be raised when an ID
       is not found in the global output list
    '''
    pass

def showIDS():
    '''Helper function to the UI customer ID queue summary.
       Formats the queue in the form of a string that is
       dispayed on the UI.
    '''
    count = 1
    outputString = ''
    for entry in OUTPUT_LIST:
        outputString += "Customer ID Queue \n" + str(count) + ' | ' + 'Customer ID: ' +  str(entry) + '\n'
        count+=1
    temp.set(outputString)
    
    

def add_entry_fields():
    '''Function mapped to the Add Customer ID button.
       Produces a summary of the customer ID queue on the
       UI when the Add Customer ID button is pressed.
    '''
    try:
        if len(e1.get()) != 7 or int(e1.get()) in OUTPUT_LIST:
            raise ValueError
        customerID = int(e1.get())
        OUTPUT_LIST.append(customerID)
        showIDS()
        master.update()
    except ValueError:
        messagebox.showinfo("Notice","Please enter a valid  7-digit customer ID.")



def remove_from_list():
    '''Function mapped to the Remove Customer ID button.
       Removes a specific customer customer ID from the
       report generation queue.
    '''
    try:
        if len(e2.get()) != 7:
            raise ValueError
        if int(e2.get()) not in OUTPUT_LIST:
            raise NonExistant
        removeID = int(e2.get())
        OUTPUT_LIST.remove(removeID)
        showIDS()
        
    except ValueError:
        messagebox.showinfo("Notice","Please enter a valid  7-digit customer ID.")
    except NonExistant:
        messagebox.showinfo("Notice","ID not found in stored Customer ID list")

### MAKE A CLASS 
def generate_reserve_report():
    '''Function mapped to the Generate Lot Distribution Report
       button. Produces an excel spreadsheet in a Data folder
       in the working directory.
    '''
    for entry in OUTPUT_LIST:
        rg.reserve_report(entry, conn)

def generate_consolidated_lot_report():
    '''Function mapped to the Generate Lot Distribution Report
       button. Produces an excel spreadsheet in a Data folder
       in the working directory.
    '''
    for entry in OUTPUT_LIST:   
        clr.consolidated_lot_report(entry, conn)

##def generate_consolidated_lot_report():
##        '''Function mapped to the Generate Lot Distribution Report
##       button. Produces an excel spreadsheet in a Data folder
##       in the working directory.
##    '''
##    for entry in OUTPUT_LIST:
##        rg.reserve_report(entry, conn)
    
if __name__ == '__main__':
        
    #MASTER WINDOW
    master = Tk()
    #MASTER WINDOW

    temp = StringVar()


    #LABEL INITIATION
    Label(master, text="Customer ID").grid(row=0, column = 0, sticky=W)
    Label(master, text="Remove ID").grid(row=1, column = 0, sticky=W)
    Label(master, textvariable = temp).grid(row = 9)
    #LABEL INITIATION

    #ENTRY FIELD INITATION
    e1 = Entry(master)
    e2 = Entry(master)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    #ENTRY FIELD INITATION


    # WORKS
    Button(master, text='Generate Lot Distribution Report', command=generate_reserve_report).grid(row=3, column=0, sticky=W, pady=4)
    # NEEDS UNIQUE OUTPUT
    Button(master, text='Generate Lot Compressed Report', command=generate_consolidated_lot_report).grid(row=4, column=0, sticky=W, pady=4)
    # NEEDS UNIQUE OUTPUT
    Button(master, text='Generate Ship-To Customer Reserve Report', command=generate_reserve_report).grid(row=5, column=0, sticky=W, pady=4)



    Button(master, text='Add Customer ID', command=add_entry_fields).grid(row=6, column=0, sticky=W, pady=4)

    Button(master, text='Remove Customer ID', command=remove_from_list).grid(row=7, column=0, sticky=W, pady=4)

    Button(master, text='Quit', command=master.destroy).grid(row=8, column=0, sticky=W, pady=4)
    database = "pythonsqlite.db"
    conn = sq.sqlite3.connect(database)


    mainloop()
