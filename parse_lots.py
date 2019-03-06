from openpyxl import load_workbook
import sqlite, sqlite3
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


database = "pythonsqlite.db"
conn = sqlite3.connect(database)

dataFolder = Path("Data")
filename = "Liquid IA Anemia data.xlsx"
file_path = str((dataFolder / filename).resolve())

sheet = load_workbook(file_path)
active_sheet = sheet.active

header_row = 0
headers = []

count = 0
for each in active_sheet:
    if (count == header_row):
        for e in each:
            headers.append(e.value)
        #print(headers)
        count = count +1
        continue

    '''
     1 | id 
     0 | product_id
     2 | manufacture_date
     4 | quantity_boxes
     5 | release_date
     6 | expiration_date
     7 | backorder_start 
     7 | backorder_end
    '''

    if (str(each[1].value) == 'None'):
        continue

    row = []
    row.append(str(each[1].value))
    row.append(str(each[0].value))
    row.append(str(each[2].value))
    row.append(str(Decimal(each[3].value/6).quantize(0, ROUND_HALF_UP)))
    row.append(str(each[5].value))
    row.append(str(each[6].value))

    if str(each[7].value) == 'None':
        row.append('')
        row.append('')
    else:
        backorder_split = str(each[7].value).split(" ")
        row.append(backorder_split[0])
        row.append(backorder_split[2])


    #print(" | ".join(row))
    sqlite.create_lot(conn, row)

conn.commit()



