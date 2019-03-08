import xlsxwriter
from pathlib import Path    # pathlib uses the correct format of path for the local OS
import os
from datetime import datetime
import helper

def generate(customer_id, conn):
    filename = 'ship_to_reserve_report_' + str(customer_id) + '.xlsx'
    # delete the next 2 lines if pathing causes error, change file_path to filename in line 12
    if not os.path.exists("GeneratedReports"):
        os.makedirs("GeneratedReports")
    exported_folder = Path("GeneratedReports/")
    file_path = str((exported_folder / filename).resolve()) # path of the generated report in string

    cur = conn.cursor()

    workbook = xlsxwriter.Workbook(file_path)   # create excel sheet
    worksheet = workbook.add_worksheet()

    # set column width
    worksheet.set_column(1, 1, 40)
    worksheet.set_column(2, 7, 10)
    worksheet.set_column(9, 9, 40)
    worksheet.set_row(5, 45)

    # set format
    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    cell_format.set_text_wrap()

    sheet_row = 0
    sheet_col = 0
    worksheet.write(sheet_row, sheet_col, "Subject:")  # row 1
    worksheet.write(sheet_row, sheet_col + 1, "SoldToParty" + customer_id)
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col + 1, "Account # " + str(customer_id))  # row 2
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "")   # row 3
    sheet_row += 1

    date_format = workbook.add_format({'num_format': 'mm/dd/yy'})
    worksheet.write(sheet_row, sheet_col, "Date:")  # row 4
    worksheet.write(sheet_row, sheet_col + 1, "=TODAY()", date_format)
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "")  # row 5
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "ITEM #", cell_format)  # row 6
    worksheet.write(sheet_row, sheet_col + 1, "DESCRIPTION", cell_format)
    worksheet.write(sheet_row, sheet_col + 2, "QTY/BOX", cell_format)
    worksheet.write(sheet_row, sheet_col + 3, "LOT #", cell_format)
    worksheet.write(sheet_row, sheet_col + 4, "EXP. DATE", cell_format)
    worksheet.write(sheet_row, sheet_col + 5, "Product Allocation", cell_format)
    worksheet.write(sheet_row, sheet_col + 6, "Shipped Quantity (Indy)", cell_format)
    worksheet.write(sheet_row, sheet_col + 7, "Remaining Allocation", cell_format)
    worksheet.write(sheet_row, sheet_col + 8, "#mos dat'g left", cell_format)
    worksheet.write(sheet_row, sheet_col + 9, "Comments", cell_format)
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "")  # row 7
    sheet_row += 1

    sql = """
                SELECT p.id, p.name, 'qty/box', r.batch_id, l.expiration_date, r.booked_qty, r.shipped_qty, r.remaining_qty,
                printf("%.1f",(julianday(l.expiration_date) - julianday(date('now')))/30.42)
                FROM product p 
                LEFT JOIN lot l on p.id = l.product_id 
                LEFT JOIN reservation r on l.id = r.batch_id
                LEFT JOIN customer c on r.ship_to_party = c.id
                WHERE l.id is not null AND c.id = """ + str(customer_id)
    cur.execute(sql)

    rows = cur.fetchall()   # return list of items from the query
    product_type = -1
    for row in rows:
        print(row)
        product = row[0]
        if (helper.isInt(product)):
            umbrella_product = int(product) - int(product)%10
            if (not (umbrella_product == product_type)):
                product_type = umbrella_product
                worksheet.write(sheet_row, sheet_col, "")
                sheet_row += 1
        elif (product_type == product):
            pass
        else:
            product_type = product
            worksheet.write(sheet_row, sheet_col, "")
            sheet_row += 1
        date_time = datetime.strptime(str(row[4]).split(' ')[0], '%Y-%m-%d')    #set date format
        worksheet.write(sheet_row, sheet_col, str(row[0]))
        worksheet.write(sheet_row, sheet_col + 1, str(row[1]))
        worksheet.write(sheet_row, sheet_col + 2, str(row[2]))
        worksheet.write(sheet_row, sheet_col + 3, str(row[3]))
        worksheet.write(sheet_row, sheet_col + 4, date_time, date_format)
        worksheet.write(sheet_row, sheet_col + 5, str(row[5]))
        worksheet.write(sheet_row, sheet_col + 6, str(row[6]))
        worksheet.write(sheet_row, sheet_col + 7, str(row[7]))
        worksheet.write(sheet_row, sheet_col + 8, '=ROUND(((-TODAY()) + $E%d)/30.42,1)' % (sheet_row+1))    # formula to calculate mos dat'g left
        worksheet.write(sheet_row, sheet_col + 9, "")
        sheet_row += 1



    workbook.close()