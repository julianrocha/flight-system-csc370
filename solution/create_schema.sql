-- Julian Rocha V00870460

-- If the tables/functions already exist, delete them --
drop table if exists reservations;
drop table if exists passengers;
drop table if exists flights;
drop table if exists aircrafts;
drop table if exists airports;

drop function if exists aircraft_capacity_trigger();
drop function if exists international_flight_trigger();

-- Create airports table --
create table airports( 
	airport_code varchar(3) primary key check(airport_code similar to '[A-Z]{3}'),
	airport_name varchar(255) not null check(airport_name != ''),
	country varchar(255) not null check(country != ''),
	international boolean not null
	);

-- Create aircrafts table --
create table aircrafts(
	aircraft_id varchar(64) primary key check(aircraft_id != ''),
	airline varchar(255) not null check(airline != ''),
	model varchar(255) not null check(model != ''),
	seating_capacity int check(seating_capacity >= 0)
	);

-- Create flights table --
create table flights(
	flight_id int primary key,
	airline varchar(255),
	src varchar(3),
	dst varchar(3),
	departure timestamp,
	arrival timestamp,
	aircraft_id varchar(64),
	foreign key (src) references airports(airport_code)
		on delete restrict
		on update restrict,
	foreign key (dst) references airports(airport_code)
		on delete restrict
		on update restrict,
	foreign key (aircraft_id) references aircrafts(aircraft_id)
		on delete restrict
		on update restrict,
	constraint different_airports check(src != dst),
	constraint chronological_order check(departure < arrival)
	-- check that flight airline matches aircraft airline
	-- check each aircraft must be on the ground for at least 60 minutes between flights
	-- check the same aircraft can’t be used for two flights at the same time
	-- check the aircraft must take off from the same airport where it landed
	);

-- Create passengers table --
create table passengers( 
		passenger_id int primary key,
		passenger_name varchar(1000) not null check(passenger_name != '')	
	);

-- Create reservations table --
create table reservations( 
		passenger_id int,
		flight_id int,
		primary key (passenger_id, flight_id),
		foreign key (passenger_id) references passengers(passenger_id)
			on delete restrict
			on update restrict,
		foreign key (flight_id) references flights(flight_id)
			on delete restrict
			on update restrict
	);


-- check the aircraft used must have a seating capacity greater than or equal to the number of existing reservations for the flight
create function aircraft_capacity_trigger()
returns trigger as
$BODY$
begin
if exists (
	select flight_id, seating_capacity, count(*)
	from reservations natural join flights natural join aircrafts
	group by flight_id, seating_capacity
	having count(*) > seating_capacity
)
then 
	raise exception 'Aircraft reservation capacity is full';
end if;
return new;
end
$BODY$
language plpgsql;

create trigger reservations_aircraft_capacity_trigger
	after insert or update on reservations
	execute procedure aircraft_capacity_trigger();

create trigger flights_aircraft_capacity_trigger
	after update on flights
	execute procedure aircraft_capacity_trigger();

create trigger aircrafts_aircraft_capacity_trigger
	after update on aircrafts
	execute procedure aircraft_capacity_trigger();


-- check that both airports are international if airports in different countries
create function international_flight_trigger()
returns trigger as
$BODY$
begin
if exists (
	select * from flights
	inner join airports as src on flights.src = src.airport_code
	inner join airports as dst on flights.dst = dst.airport_code
	where src.country != dst.country and not (src.international and dst.international)
)
then 
	raise exception 'International flights not supported for these airports';
end if;
return new;
end
$BODY$
language plpgsql;

create trigger flights_international_flight_trigger
	after insert or update on flights
	execute procedure international_flight_trigger();

create trigger airports_international_flight_trigger
	after update on airports
	execute procedure international_flight_trigger();



select * from airports;
select * from aircrafts;
select * from flights;
select * from passengers;
select * from reservations;


