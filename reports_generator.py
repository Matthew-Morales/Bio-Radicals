import xlsxwriter

def reserve_report(customer_id, conn):
    cur = conn.cursor()

    workbook = xlsxwriter.Workbook('customer' + str(customer_id) + '.xlsx')
    worksheet = workbook.add_worksheet()
    sheet_row = 0
    sheet_col = 0
    worksheet.write(sheet_row, sheet_col, "Subject:")
    worksheet.write(sheet_row, sheet_col + 1, "Customer1")
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col + 1, "Account # " + str(customer_id))
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "")
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "Date:")
    worksheet.write(sheet_row, sheet_col + 1, "Date")
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "")
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "ITEM #")
    worksheet.write(sheet_row, sheet_col + 1, "DESCRIPTION")
    worksheet.write(sheet_row, sheet_col + 2, "QTY/BOX")
    worksheet.write(sheet_row, sheet_col + 3, "LOT #")
    worksheet.write(sheet_row, sheet_col + 4, "EXP. DATE")
    worksheet.write(sheet_row, sheet_col + 5, "Product Allocation")
    worksheet.write(sheet_row, sheet_col + 6, "Shipped Quantity (Indy)")
    worksheet.write(sheet_row, sheet_col + 7, "Remaining Allocation")
    worksheet.write(sheet_row, sheet_col + 8, "#mos dat'g left")
    worksheet.write(sheet_row, sheet_col + 9, "Comments")
    sheet_row += 1

    worksheet.write(sheet_row, sheet_col, "")
    sheet_row += 1

    cur.execute(
        """
        select p.id, p.name, 'qty/box', l.id, l.expiration_date, r.booked_qty, r.shipped_qty, r.remaining_qty,
        printf("%.1f",(julianday(l.expiration_date) - julianday(date('now')))/30.42)
        from product p 
        left join lot l on l.product_id = p.id
        left join reservation r on r.batch_id = l.id
        left join customer c on c.id = r.sold_to_party
        where c.id =""" + str(customer_id))
    '''
    cur.execute(
        """
        select p.id, p.name, 'qty/box', l.id, l.expiration_date, r.booked_qty, r.shipped_qty, r.remaining_qty,
        printf("%.1f",(julianday(l.expiration_date) - julianday(date('now')))/30.42)
        from customer c
        left join reservation r on r.sold_to_party = c.id
        left join lot l on l.id = r.batch_id
        left join product p on p.id = l.product_id
        where c.id =""" + str(customer_id)

    )
    '''
    rows = cur.fetchall()
    for row in rows:
        print(row)

        worksheet.write(sheet_row, sheet_col, str(row[0]))
        worksheet.write(sheet_row, sheet_col + 1, str(row[1]))
        worksheet.write(sheet_row, sheet_col + 2, str(row[2]))
        worksheet.write(sheet_row, sheet_col + 3, str(row[3]))
        worksheet.write(sheet_row, sheet_col + 4, str(row[4]).split(' ')[0])
        worksheet.write(sheet_row, sheet_col + 5, str(row[5]))
        worksheet.write(sheet_row, sheet_col + 6, str(row[6]))
        worksheet.write(sheet_row, sheet_col + 7, str(row[7]))
        worksheet.write(sheet_row, sheet_col + 8, str(row[8]))
        worksheet.write(sheet_row, sheet_col + 9, "")
        sheet_row += 1

        worksheet.write(sheet_row, sheet_col, "")
        sheet_row += 1

    workbook.close()