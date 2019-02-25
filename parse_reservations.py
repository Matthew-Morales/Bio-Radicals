from openpyxl import load_workbook
import sqlite, sqlite3

database = "pythonsqlite.db"
conn = sqlite3.connect(database)

sheet = load_workbook("rReport.xlsx")
active_sheet = sheet.active

header_row = 0
headers = []
salesperson_fullname = []
products = []

count = 0
for each in active_sheet:
    if (count == header_row):
        for e in each:
            headers.append(e.value)
        #print(headers)
        count = count +1
        continue


    '''
    auto-increment | id integer 
    0 | sold_to_party
    2 | ship_to_party
    4 | sales_rep
    7 | batch_id
    9 | booked qty
    10 | shipped qty
    11 | remaining qty
    '''

    row = []
    row.append(str(each[0].value))
    row.append(str(each[2].value))
    row.append(str(each[4].value))
    row.append(str(each[7].value))
    row.append(str(each[9].value))
    row.append(str(each[10].value))
    row.append(str(each[11].value))

    sqlite.create_reservation(conn, row)


    if str(each[4].value) not in salesperson_fullname:
        salesperson_fullname.append(str(each[4].value))

    '''
    5 | Material #
    6 | Name
    '''
    if (str(each[5].value), str(each[6].value)) not in products:
        products.append((str(each[5].value), str(each[6].value)))

    print(" | ".join(row))

conn.commit()

for fullname in salesperson_fullname:
    #print(fullname)
    sqlite.create_salesperson_fullname(conn, (None, fullname))

for product in products:
    #print(product)
    sqlite.create_product(conn, product)

conn.commit()