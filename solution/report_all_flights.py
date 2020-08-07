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
    
#Mockup: Print details for two flights 
print_entry(10,'WestJet','Vancouver International Airport','Victoria International Airport','2020-06-29 09:24','2020-06-29 09:55',31,'A1233','Dehavilland DHC-8',70,35)
print_entry(12,'Air Canada','Vancouver International Airport','Lester B. Pearson International Airport','2020-06-29 15:00','2020-06-29 19:20',260,'A1234','Boeing 737-300',140,101)