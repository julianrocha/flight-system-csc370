# manage_reservations.py
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

with open(input_filename) as f:
    for row in csv.reader(f):
        if len(row) == 0:
            continue #Ignore blank rows
        if len(row) != 4:
            print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
			#Maybe abort the active transaction and roll back at this point?
			break
        action,flight_id,passenger_id,passenger_name = row
        
        if action.upper() not in ('CREATE','DELETE'):
            print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
			#Maybe abort the active transaction and roll back at this point?
			break
        
		#Do something with the data here
		#Make sure to catch any exceptions that occur and roll back the transaction if a database error occurs.
		
		