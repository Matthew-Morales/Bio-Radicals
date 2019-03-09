import xlsxwriter
from pathlib import Path    # pathlib uses the correct format of path for the local OS
import os
from datetime import datetime
import helper
def consolidated_lot_report(customer_id, conn):
    filename = 'customer' + str(customer_id) + '.xlsx'
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
    worksheet.write(sheet_row, sheet_col + 1, "Customer1")
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col + 1, "Account # " + str(customer_id))  # row 2
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "")   # row 3
    sheet_row += 1
    ### DATE FORMAT FOR EXP
    date_format = workbook.add_format({'num_format': 'mm/dd/yy'})
    ### DATE FORMAT FOR EXP

    ###DATE FORMAT FOR CURRENT DATE 
    current_date_format = workbook.add_format({'num_format': 'mmm d, yyyy'})
    ###DATE FORMATE FOR CURRENT DATE
    worksheet.write(sheet_row, sheet_col, "Date:")  # row 4
    worksheet.write(sheet_row, sheet_col + 1, "=TODAY()", current_date_format)
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
###CHANGES TO B MADE HERE ###
    sql = """
                SELECT p.id, p.name, 'qty/box', r.ship_to_party, c2.name, r.batch_id, l.expiration_date,  SUM(r.booked_qty), SUM(r.shipped_qty), SUM(r.remaining_qty),
                printf("%.1f",(julianday(l.expiration_date) - julianday(date('now')))/30.42)
                FROM product p
                LEFT JOIN lot l on p.id = l.product_id 
                LEFT JOIN reservation r on l.id = r.batch_id
                LEFT JOIN customer c on r.sold_to_party = c.id
                LEFT JOIN customer c2 on r.ship_to_party = c2.id
                WHERE l.id is not null AND c.id = {0}
                GROUP BY r.batch_id
                ORDER BY l.expiration_date;
                """.format(str(customer_id))
    cur.execute(sql)

    rows = cur.fetchall()   # return list of items from the query
    product_type =-1
    for row in rows:
        print(row)
        product = row[5]
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
        date_time = datetime.strptime(str(row[6]).split(' ')[0], '%Y-%m-%d')    #set date format
        worksheet.write(sheet_row, sheet_col, str(row[0]))
        worksheet.write(sheet_row, sheet_col + 1, str(row[1]))
        worksheet.write(sheet_row, sheet_col + 2, str(row[2]))
        worksheet.write(sheet_row, sheet_col + 3, str(row[5]))
        worksheet.write(sheet_row, sheet_col + 4, date_time, date_format)
        worksheet.write(sheet_row, sheet_col + 5, str(row[7]))
        worksheet.write(sheet_row, sheet_col + 6, str(row[8]))
        worksheet.write(sheet_row, sheet_col + 7, str(row[9]))
        worksheet.write(sheet_row, sheet_col + 8, '=ROUND(((-TODAY()) + $E%d)/30.42,1)' % (sheet_row+1))    # formula to calculate mos dat'g left
        worksheet.write(sheet_row, sheet_col + 9, "")

        #sheet_row += 1
        #worksheet.write(sheet_row, sheet_col, "")
        sheet_row += 1

    workbook.close()

'''
SELECT
   r.batch_id,
   SUM(r.booked_qty) AS r.booked_qty,
   SUM(r.shipped_qty) AS r.shipped_qty,
   SUM(r.remaining_qty) AS r.remaining_qty
FROM product p
GROUP BY r.batch_id;
'''

