# DE-Zoomcamp 2024 - Week 1

# Homework
1. Tag that automatically removes the container when it exits;
```commandline
docker run --rm
```

2. I get version of wheel as 0.44.0
```commandline
docker run --entrypoint bash -it python:3.9
pip list
```

3. There were 15,612 taxi trips both started and finished on 18th Sept 2019. 
```
SELECT COUNT(*)
FROM green_taxi_trips
WHERE 
	DATE(lpep_pickup_datetime) = '2019-09-18' AND
	DATE(lpep_dropoff_datetime) = '2019-09-18'
```

4. The date '2019-09-26' was the day with the longest trip.

```
SELECT DATE(lpep_pickup_datetime), MAX(trip_distance) AS trip_d
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) IN ('2019-09-18', '2019-09-16', '2019-09-26', '2019-09-21')
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY trip_d DESC
```

5.  Brooklyn, Manhattan and Queens each had a total sum of amount greater than 50,000

```
SELECT zpu."Borough", SUM(t.total_amount)
FROM green_taxi_trips t,
	zones zpu
WHERE zpu."LocationID" = t."PULocationID" AND 
	NOT zpu."Borough" = 'Unknown' AND
	DATE(t.lpep_pickup_datetime) = '2019-09-18'
GROUP BY zpu."Borough"
```

6. JFK Airport had the largest tip of $62.31

```
SELECT zdo."Zone", MAX(t.tip_amount) as max_tip
FROM green_taxi_trips t
JOIN zones zdo ON zdo."LocationID" = t."DOLocationID"
	JOIN zones zpu ON  zpu."LocationID" = t."PULocationID"
WHERE zpu."LocationID" = t."PULocationID" AND 
		zpu."Zone" = 'Astoria' 
		AND DATE(t.lpep_pickup_datetime) BETWEEN '2019-09-01' AND '2019-10-01'
GROUP BY zdo."Zone"
ORDER BY max_tip DESC
```