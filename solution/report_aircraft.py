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
    
    
#Mockup: Print details for two aircraft
print_entry('A1234','Air Canada','Boeing 737-300',0,0,0,140)
print_entry('A1235','Air Canada','Boeing 777-333ER',10,100,16.7,140)