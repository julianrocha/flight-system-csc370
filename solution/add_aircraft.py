# add_aircraft.py
# CSC 370 - Summer 2020 - Starter code for Assignment 6
#
#
# B. Bird - 06/28/2020

import sys, csv, psycopg2

if len(sys.argv) < 2:
    print("Usage: %s <input file>"%sys.argv[0],file=sys.stderr)
    sys.exit(1)
    
input_filename = sys.argv[1]

# Open your DB connection here
psql_user = 'julianrocha'
psql_db = 'julianrocha'
psql_password = 'V00870460'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()
cursor.execute('set constraints all deferred;')

with open(input_filename) as f:
    for row in csv.reader(f):
        if len(row) == 0:
            continue #Ignore blank rows
        if len(row) != 4:
            print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
            conn.rollback()
            break
        aircraft_id, airline, model, seating_capacity = row
        try:
            cursor.execute("insert into aircrafts values( %s, %s, %s, %s );", (aircraft_id, airline, model, seating_capacity) )
        except psycopg2.ProgrammingError as err: 
            #ProgrammingError is thrown when the database error is related to the format of the query (e.g. syntax error)
            print("Caught a ProgrammingError:",file=sys.stderr)
            print(err,file=sys.stderr)
            conn.rollback()
            break
        except psycopg2.IntegrityError as err: 
            #IntegrityError occurs when a constraint (primary key, foreign key, check constraint or trigger constraint) is violated.
            print("Caught an IntegrityError:",file=sys.stderr)
            print(err,file=sys.stderr)
            conn.rollback()
            break
        except psycopg2.InternalError as err:  
            #InternalError generally represents a legitimate connection error, but may occur in conjunction with user defined functions.
            #In particular, InternalError occurs if you attempt to continue using a cursor object after the transaction has been aborted.
            #(To reset the connection, run conn.rollback() and conn.reset(), then make a new cursor)
            print("Caught an IntegrityError:",file=sys.stderr)
            print(err,file=sys.stderr)
            conn.rollback()
            break
try:
    conn.commit()
except psycopg2.IntegrityError as err: 
    #IntegrityError occurs when a constraint (primary key, foreign key, check constraint or trigger constraint) is violated.
    print("Caught an IntegrityError:",file=sys.stderr)
    print(err,file=sys.stderr)
except psycopg2.InternalError as err:  
    print("Caught an IntegrityError:",file=sys.stderr)
    print(err,file=sys.stderr)
cursor.close()
conn.close()    