import sqlite3
import sqlite

#products to dummy
#00105C, 00108B,
#27114, 27115, 27116

database = "pythonsqlite.db"
conn = sqlite3.connect(database)

#create lots
#be sure the lot chosen doesn't already exist
#lot (id, product_id, manufacture_date, quantity_boxes, release_date, expiration_date,
#     backorder_start, backorder_end)

#since there aren't that many lots yet
#lot ids will be almost the lot# + 1 or 2
lot_00105C_1 = ["001051", "00105C", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_00105C_2 = ["001052", "00105C", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_00108B_1 = ["001081", "00108B", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_00108B_2 = ["001082", "00108B", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_27114_1 = ["271141", "27114", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_27114_2 = ["271142", "27114", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_27115_1 = ["271151", "27115", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_27115_2 = ["271152", "27115", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_27116_1 = ["271161", "27116", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]
lot_27116_2 = ["271162", "27116", "2018-12-31 00:00:00", "10", "2018-01-14 00:00:00", "2020-12-31 00:00:00", "", ""  ]

lots = [lot_00105C_1,lot_00105C_2, lot_00108B_1, lot_00108B_2, lot_27114_1, lot_27114_2, lot_27115_1, lot_27115_2, lot_27116_1, lot_27116_2]

for lot in lots:
    print(lot)
    sqlite.create_lot(conn, lot)
conn.commit()
#create reservation
#choose 1003151 as customer since they already have data
#reservation (sold_to_party, ship_to_party, sales_rep, batch_id, booked_qty, shipped_qty, remaining_qty)
reservation_0 = ['1003151', '', '', '001051', '10', '0', '10']
reservation_1 = ['1003151', '', '', '001052', '10', '0', '10']
reservation_2 = ['1003151', '', '', '001081', '10', '0', '10']
reservation_3 = ['1003151', '', '', '001082', '10', '0', '10']
reservation_4 = ['1003151', '', '', '271141', '10', '0', '10']
reservation_5 = ['1003151', '', '', '271142', '10', '0', '10']
reservation_6 = ['1003151', '', '', '271151', '10', '0', '10']
reservation_7 = ['1003151', '', '', '271152', '10', '0', '10']
reservation_8 = ['1003151', '', '', '271161', '10', '0', '10']
reservation_9 = ['1003151', '', '', '271162', '10', '0', '10']

reservations = [reservation_0, reservation_1, reservation_2, reservation_3, reservation_4, reservation_5, reservation_6, reservation_7, reservation_8, reservation_9]

for reservation in reservations:
    print(reservation)
    sqlite.create_reservation(conn, reservation)
conn.commit()