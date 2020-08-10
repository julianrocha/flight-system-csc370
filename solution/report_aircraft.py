# report_all_flights.py
# CSC 370 - Summer 2020 - Starter code for Assignment 6
#
#
# B. Bird - 06/29/2020

import psycopg2, sys



def print_entry(aircraft_id, airline, model_name, num_flights, flight_hours, avg_seats_full, seating_capacity):
    print("%-5s (%s): %s"%(aircraft_id, model_name, airline))
    print("    Number of flights : %d"%num_flights)
    print("    Total flight hours: %d"%flight_hours)
    print("    Average passengers: (%.2f/%d)"%(avg_seats_full,seating_capacity))
    

# Open your DB connection here
psql_user = 'julianrocha'
psql_db = 'julianrocha'
psql_password = 'V00870460'
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

cursor.execute("""
with
	aircraft_summaries as(
		select
			aircrafts.aircraft_id, aircrafts.airline, model, seating_capacity,
			coalesce(round(sum((extract(epoch from arrival) - extract(epoch from departure))/ 3600)), 0) as flight_hours,
			count(flight_id) as num_flights
		from aircrafts
		left join flights using(aircraft_id)
		group by aircrafts.aircraft_id, aircrafts.airline, model, seating_capacity
		order by aircrafts.aircraft_id),
	avg_capacities as(
		select aircraft_id, round(avg(flight_count), 2) as avg_seats_full
		from(
			select flight_id, aircraft_id, count(passenger_id) as flight_count from flights left join reservations using(flight_id) group by flight_id, aircraft_id
		) as flight_counts
		group by aircraft_id)
select
	aircraft_id,
	airline,
	model as model_name,
	num_flights,
	flight_hours,
	coalesce(avg_seats_full, 0) as avg_seats_full,
	seating_capacity
from aircraft_summaries left join avg_capacities using(aircraft_id)
order by aircraft_id;
""")

rows_found = 0
while True:
	row = cursor.fetchone()
	if row is None:
		break
	rows_found += 1
	aircraft_id = row[0]
	airline = row[1]
	model_name = row[2]
	num_flights = row[3]
	flight_hours = row[4]
	avg_seats_full = row[5]
	seating_capacity = row[6]
	print_entry(aircraft_id, airline, model_name, num_flights, flight_hours, avg_seats_full, seating_capacity)

cursor.close()
conn.close()