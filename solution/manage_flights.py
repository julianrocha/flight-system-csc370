# manage_flights.py
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
        action = row[0]
        if action.upper() == 'DELETE':
            if len(row) != 2:
                print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
                conn.rollback()
                break
            flight_id = row[1]
            cursor.execute("delete from flights where flight_id = %s;", (flight_id,))
        elif action.upper() in ('CREATE','UPDATE'):
            if len(row) != 8:
                print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
                conn.rollback()
                break
            flight_id = row[1]
            airline = row[2]
            src,dest = row[3],row[4]
            departure, arrival = row[5],row[6]
            aircraft_id = row[7]

            try:
                if action.upper() == 'CREATE':
                    cursor.execute("insert into flights values (%s,%s,%s,%s,%s,%s,%s);", (flight_id, airline, src, dest, departure, arrival,aircraft_id))
                elif action.upper() == 'UPDATE':
                    cursor.execute("update flights set airline=%s, src=%s, dst=%s, departure=%s, arrival=%s, aircraft_id=%s where flight_id=%s;", (airline, src, dest, departure, arrival,aircraft_id, flight_id))
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
        else:
            print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
            conn.rollback()
            break

conn.commit()
cursor.close()
conn.close()
