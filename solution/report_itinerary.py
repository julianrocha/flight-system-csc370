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


''' The lines below would be helpful in your solution
if len(sys.argv) < 2:
    print('Usage: %s <passenger id>'%sys.argv[0], file=sys.stderr)
    sys.exit(1)
'''
    
# Mockup: Print itinerary for passenger 12345 (Rebecca Raspberry)
passenger_id = 12345
passenger_name = 'Rebecca Raspberry'
print_header(passenger_id, passenger_name)
print_entry(10,'WestJet','Vancouver International Airport','Victoria International Airport','2020-06-29 09:24','2020-06-29 09:55',31,'A1233','Dehavilland DHC-8')
print_entry(12,'Air Canada','Vancouver International Airport','Lester B. Pearson International Airport','2020-06-29 15:00','2020-06-29 19:20',260,'A1234','Boeing 737-300')