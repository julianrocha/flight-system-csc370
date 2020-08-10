# report_all_flights.py
# CSC 370 - Summer 2020 - Starter code for Assignment 6
#
#
# B. Bird - 06/29/2020

import psycopg2, sys



def print_entry(flight_id, airline, source_airport_name, dest_airport_name, departure_time, arrival_time, duration_minutes, aircraft_id, aircraft_model, seating_capacity, seats_full):
    print("Flight %s (%s):"%(flight_id,airline))
    print("    [%s] - [%s] (%s minutes)"%(departure_time,arrival_time,duration_minutes))
    print("    %s -> %s"%(source_airport_name,dest_airport_name))
    print("    %s (%s): %s/%s seats booked"%(aircraft_id, aircraft_model,seats_full,seating_capacity))

# Open your DB connection here
psql_user = 'julianrocha'
psql_db = 'julianrocha'
psql_password = 'V00870460'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

cursor.execute("""
select
	flight_id,
	flights.airline,
	src.airport_name as source_airport_name,
	dst.airport_name as dest_airport_name,
	departure as departure_time,
	arrival as arrival_time,
	round((extract(epoch from arrival) - extract(epoch from departure)) / 60)::integer as duration_minutes,
	flights.aircraft_id,
	model as aircraft_model,
	seating_capacity,
	coalesce(flight_reservations.seats_full, 0)
from flights
inner join aircrafts using(aircraft_id)
inner join airports as src on flights.src = src.airport_code 
inner join airports as dst on flights.dst = dst.airport_code
left join (
	select flight_id, count(*) as seats_full from flights natural join reservations group by flight_id
) as flight_reservations using(flight_id)
order by departure, flight_id;
""")

rows_found = 0
while True:
	row = cursor.fetchone()
	if row is None:
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
	seating_capacity = row[9]
	seats_full = row[10]
	print_entry(flight_id, airline, source_airport_name, dest_airport_name, departure_time, arrival_time, duration_minutes, aircraft_id, aircraft_model, seating_capacity, seats_full)

cursor.close()
conn.close()