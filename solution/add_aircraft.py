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

# Make sure tunnel is setup
# ssh -L 55555:studdb2.csc.uvic.ca:5432 julianrocha@dblinux.csc.uvic.ca

psql_user = 'julianrocha' #Change this to your username
psql_db = 'julianrocha' #Change this to your personal DB name
psql_password = None #Put your password (as a string) here
psql_server = 'localhost'
psql_port = 55555

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)

cursor = conn.cursor()

'''
with open(input_filename) as f:
    for row in csv.reader(f):
        if len(row) == 0:
            continue #Ignore blank rows
        if len(row) != 4:
            print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
			#Maybe abort the active transaction and roll back at this point?
			break
        aircraft_id, airline, model, seating_capacity = row
        
		#Do something with the data here
		#Make sure to catch any exceptions that occur and roll back the transaction if a database error occurs.
'''