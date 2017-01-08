-- Order of view creation matters!

DROP VIEW IF EXISTS stops_filtered CASCADE;

CREATE VIEW stops_filtered AS 
	SELECT s.* 
	FROM gtfs_stops AS s 
	INNER JOIN kraje_stops AS ks ON s.stop_id = ks.stop_id 
	WHERE kraj_id=(SELECT kraj FROM kraj_filter);

CREATE VIEW stop_times_filtered AS
	SELECT DISTINCT st.* 
	FROM gtfs_stop_times AS st
	INNER JOIN stops_filtered AS s ON st.stop_id = s.stop_id;

CREATE VIEW trips_filtered AS
	SELECT DISTINCT t.* 
	FROM gtfs_trips AS t
	INNER JOIN stop_times_filtered AS st ON t.trip_id = st.trip_id;

CREATE VIEW routes_filtered AS
	SELECT DISTINCT r.*
	FROM gtfs_routes AS r
	INNER JOIN trips_filtered AS t ON t.route_id = r.route_id;

CREATE VIEW agency_filtered AS
	SELECT DISTINCT r.*
	FROM gtfs_agency AS a
	INNER JOIN routes_filtered AS r ON r.agency_id = a.agency_id;

CREATE VIEW calendar_filtered AS
	SELECT DISTINCT c.*
	FROM gtfs_calendar AS c
	INNER JOIN trips_filtered AS t ON t.service_id = c.service_id;

CREATE VIEW calendar_dates_filtered AS
	SELECT DISTINCT cd.*
	FROM gtfs_calendar_dates AS cd
	INNER JOIN trips_filtered AS t ON t.service_id = cd.service_id;
