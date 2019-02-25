import sqlite3
import xlsxwriter
import reports_generator
from sqlite3 import Error


'''
TODO:
Task 1: Edit lot, product, or reservation table to include QTY/BOX field
Task 2: Put excel creation into it's own function/class
Task 3: Remove traces of salesperson username
'''

#creates database connection - don't use it, doesn't work
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

#default table creator
#create_table_sql - a string sql statement to create a table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# ==== Creates Table Entries ====
def create_order(conn, order):
    sql = ''' INSERT INTO orders (doc_id, doc_date, sold_to_party, item, batch_id, status, 
                                  delivered_date, order_quantity, confirm_quantity, created)
              VALUES (?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, order)
    return cur.lastrowid

def create_product(conn, product):
    sql = ''' INSERT INTO product (id, name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, product)
    return cur.lastrowid

def create_customer(conn, customer):
    sql = ''' INSERT INTO customer (id, name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    return cur.lastrowid

def create_salesperson_username(conn, salesperson):
    sql = ''' INSERT INTO salesperson (username, full_name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, salesperson)
    return cur.lastrowid

def create_salesperson_fullname(conn, salesperson):
    sql = ''' INSERT INTO salesperson (username, full_name)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, salesperson)
    return cur.lastrowid

def create_lot(conn, lot):
    sql = ''' INSERT INTO lot (id, product_id, manufacture_date, quantity_boxes, release_date, expiration_date, 
                               backorder_start, backorder_end)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, lot)
    return cur.lastrowid

def create_reservation(conn, reservation):
    sql = ''' INSERT INTO reservation (sold_to_party, ship_to_party, sales_rep, batch_id, booked_qty, shipped_qty, remaining_qty)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, reservation)
    return cur.lastrowid


# ==== Other DB Queries ====
def select_all_from_table(conn, table):
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table)

    rows = cur.fetchall()

    for row in rows:
        print(row)

# ------------------------

if __name__ == '__main__':
    sql_create_product_table = """
                                    CREATE TABLE IF NOT EXISTS product (
                                        id text PRIMARY KEY, 
                                        name text
                                    );
                                """

    sql_create_customer_table = """
                                    CREATE TABLE IF NOT EXISTS customer (
                                        id text PRIMARY KEY, 
                                        name text
                                    );
                                """

    sql_create_salesperson_table = """
                                        CREATE TABLE IF NOT EXISTS salesperson (
                                            id INTEGER PRIMARY KEY, 
                                            username text, 
                                            full_name text
                                        );
                                    """

    sql_create_lot_table = """
                               CREATE TABLE IF NOT EXISTS lot (
                                    id integer PRIMARY KEY, 
                                    product_id integer,
                                    manufacture_date text,
                                    quantity_boxes integer, 
                                    release_date text, 
                                    expiration_date text, 
                                    backorder_start text, 
                                    backorder_end,
                                    FOREIGN KEY (product_id) REFERENCES product (id)
                                );
                            """

    sql_create_reservation_table = """
                                        CREATE TABLE IF NOT EXISTS reservation (
                                          id integer PRIMARY KEY, 
                                          sold_to_party integer, 
                                          ship_to_party integer, 
                                          sales_rep text, 
                                          batch_id integer, 
                                          booked_qty integer, 
                                          shipped_qty integer, 
                                          remaining_qty integer,
                                          FOREIGN KEY (sold_to_party) REFERENCES customer (id), 
                                          FOREIGN KEY (sales_rep) REFERENCES salesperson (full_name),
                                          FOREIGN KEY (batch_id) REFERENCES lot (id)
                                      );
                                    """

    sql_create_orders_table = """ 
                                        CREATE TABLE IF NOT EXISTS orders (
                                          doc_id integer,
                                          doc_date text, 
                                          sold_to_party integer, 
                                          item integer, 
                                          batch_id integer, 
                                          status text, 
                                          delivered_date text, 
                                          order_quantity integer, 
                                          confirm_quantity integer, 
                                          created text, 
                                          FOREIGN KEY (sold_to_party) REFERENCES customer (id), 
                                          FOREIGN KEY (batch_id) REFERENCES lot (id), 
                                          FOREIGN KEY (created) REFERENCES salesperson (username)
                                        );

                                    """

    database = "pythonsqlite.db"
    conn = sqlite3.connect(database)

    ''' REMEMBER TO COMMIT [ conn.commit() ]'''
    if conn is not None:
        create_table(conn, sql_create_product_table)
        create_table(conn, sql_create_customer_table)
        create_table(conn, sql_create_salesperson_table)
        create_table(conn, sql_create_lot_table)
        create_table(conn, sql_create_reservation_table)
        create_table(conn, sql_create_orders_table)



        # Example customer ids: 1001883, 1000239, 1000005
        reports_generator.reserve_report(1000005, conn)


    else:
        print("Error! cannot create the database connection.")



#http://www.sqlitetutorial.net/sqlite-python/