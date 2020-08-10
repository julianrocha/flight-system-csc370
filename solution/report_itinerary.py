# report_itinerary.py
# CSC 370 - Summer 2020 - Starter code for Assignment 6
#
#
# B. Bird - 06/28/2020

import psycopg2, sys



def print_header(passenger_id, passenger_name):
    print("Itinerary for %s (%s)"%(str(passenger_id), str(passenger_name)) )
    
def print_entry(flight_id, airline, source_airport_name, dest_airport_name, departure_time, arrival_time, duration_minutes, aircraft_id, aircraft_model):
    print("Flight %-4s (%s):"%(flight_id, airline))
    print("    [%s] - [%s] (%s minutes)"%(departure_time, arrival_time,duration_minutes))
    print("    %s -> %s (%s: %s)"%(source_airport_name, dest_airport_name, aircraft_id, aircraft_model))


if len(sys.argv) < 2:
    print('Usage: %s <passenger id>'%sys.argv[0], file=sys.stderr)
    sys.exit(1)
    
passenger_id = sys.argv[1]

# Open your DB connection here
psql_user = 'julianrocha'
psql_db = 'julianrocha'
psql_password = 'V00870460'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

cursor.execute("select * from passengers where passenger_id = %s", (passenger_id,))
row = cursor.fetchone()
if row is None:
	print("Error: Passenger %s does not exist"%passenger_id, file=sys.stderr)
	cursor.close()
	conn.close()
	sys.exit(1)
passenger_name = row[1]
print_header(passenger_id, passenger_name)

cursor.execute("""
select
	flight_id,
	flights.airline,
	src.airport_name as source_airport_name,
	dst.airport_name as dest_airport_name,
	departure as departure_time,
	arrival as arrival_time,
	round((extract(epoch from arrival) - extract(epoch from departure))/60)::integer as duration_minutes,
	aircraft_id,
	model as aircraft_model
from reservations
natural join passengers
natural join flights
inner join airports as src on src.airport_code = flights.src
inner join airports as dst on dst.airport_code = flights.dst
inner join aircrafts using(aircraft_id)
where passenger_id = %s
order by departure, flight_id;
""", (passenger_id,))

rows_found = 0
while True:
	row = cursor.fetchone()
	if row is None:
		if rows_found == 0:
			print("Error: Passenger %s has no reserved flights"%passenger_id, file=sys.stderr)
			cursor.close()
			conn.close()
			sys.exit(1)
		break
	rows_found += 1
	flight_id = row[0]
	airline = row[1]
	source_airport_name = row[2]
	dest_airport_name = row[3]
	departure_time = row[4]
	arrival_time = row[5]
	duration_minutes = row[6]
	aircraft_id = row[7]
	aircraft_model = row[8]
	print_entry(flight_id, airline, source_airport_name, dest_airport_name, departure_time, arrival_time, duration_minutes, aircraft_id, aircraft_model)

cursor.close()
conn.close()