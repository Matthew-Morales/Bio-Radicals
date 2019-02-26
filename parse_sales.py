from openpyxl import load_workbook
import sqlite, sqlite3
from pathlib import Path


database = "pythonsqlite.db"
conn = sqlite3.connect(database)

dataFolder = Path("Data")
filename = "anemiasales.xlsx"
file_path = str((dataFolder / filename).resolve())

sheet = load_workbook(file_path)
active_sheet = sheet.active

header_row = 6
headers = []
salesperson_username = []

count = 0
for each in active_sheet:
    #gets the column headers
    if (count == header_row):
        for e in each:
            headers.append(e.value)
        #print(headers)

    #skips all the beginning stuff before the actual data
    if (count <= header_row + 1):
        count += 1
        continue

    '''
    lot table columns
    2 | doc_id 
    0 | doc_date
    4 | sold_to_party
    6 | item
    9 | batch_id
    13 | status
    17 | delivered_date
    14 | order_quantity
    15 | confirm_quantity
    19 | created
    '''
    #gets row data and prints it
    row = []
    row.append(str(each[2].value))
    row.append(str(each[0].value))
    row.append(str(each[4].value))
    row.append(str(each[6].value))
    row.append(str(each[9].value))
    row.append(str(each[13].value))
    row.append(str(each[17].value))
    row.append(str(each[14].value))
    row.append(str(each[15].value))
    row.append(str(each[19].value))

    #list of salespersons usernames
    if str(each[19].value) not in salesperson_username:
        salesperson_username.append(str(each[19].value))

    #print(" | ".join(row))
    sqlite.create_order(conn, row)

    count += 1
conn.commit()

#print(salesperson_username)
for username in salesperson_username:
    sqlite.create_salesperson_username(conn, (username, None))
conn.commit()
