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

3. There were 490,350 taxi trips both started and finished on 18th Sept 2019. 
```
SELECT COUNT(*)
FROM yellow_taxi_trips
WHERE 
	DATE(tpep_pickup_datetime) BETWEEN '2019-09-18' AND '2019-09-19' AND
	DATE(tpep_dropoff_datetime) BETWEEN '2019-09-18' AND '2019-09-19'
```

4. The date '2019-09-16' was the day with the longest trip.

```
SELECT DATE(tpep_pickup_datetime), MAX(trip_distance) AS trip_d
FROM yellow_taxi_trips
WHERE DATE(tpep_pickup_datetime) IN ('2019-09-18', '2019-09-16', '2019-09-26', '2019-09-21')
GROUP BY DATE(tpep_pickup_datetime)
ORDER BY trip_d DESC
```

5.  Brooklyn, Manhattan and Queens each had a total sum of amount greater than 50,000

```
SELECT zpu."Borough", SUM(t.total_amount)
FROM yellow_taxi_trips t,
	zones zpu
WHERE zpu."LocationID" = t."PULocationID" AND 
	NOT zpu."Borough" = 'Unknown' AND
	DATE(t.tpep_pickup_datetime) = '2019-09-18'
GROUP BY zpu."Borough"
```

6. JFK Airport had the largest tip of $13.20

```
SELECT zdo."Zone", MAX(t.tip_amount) as max_tip
FROM yellow_taxi_trips t
JOIN zones zdo ON zdo."LocationID" = t."DOLocationID"
	JOIN zones zpu ON  zpu."LocationID" = t."PULocationID"
WHERE zpu."LocationID" = t."PULocationID" AND 
		zpu."Zone" = 'Astoria' 
		AND DATE(t.tpep_pickup_datetime) BETWEEN '2019-09-01' AND '2019-10-01'
GROUP BY zdo."Zone"
ORDER BY max_tip DESC
```


This README servers as my course notes when running commands on Ubuntu for me and others students to refer back to.

Ensuring Docker is installed:

```console
docker --version
```

## 1. Running Python in Docker
Start a Python Docker container

Run a Python container interactively (-it):

```commandline
docker run -it python:3.11
```
Start a Python container with bash (for pip and other commands..):

```commandline
docker run -it --entrypoint bash python:3.11
```

## 2. Useful Docker Commands
List running Docker containers
```commandline
docker ps
```
List Docker networks
```commandline
docker network ls
```

Inspect a Docker network

Replace {name} with the name of the network:

```commandline
docker network inspect {name}
```

3. Setting up PostgreSQL and pgAdmin with Docker
### Run a PostgreSQL container

This command will run a PostgreSQL container with the following settings:

    Username: root
    Password: root
    Database: ny_taxi
    Volume mount: ny_taxi_postgres_data
    Port: 5432
    Docker network: pg-network

```commandline
docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name=pg-database \
    postgres:13
```

### Run pgAdmin

To manage the PostgreSQL database via a web UI, use pgAdmin:

```commandline
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=pg-network \
    --name=pgadmin \
    dpage/pgadmin4
```

Access pgAdmin by navigating to localhost:8080 in your browser.
## 4. Ingesting Data into PostgreSQL
Download Data

Yellow trip data;
 ```commandline
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz"
```
Taxi Zone Lookup Table:
```commandline
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
```
Ingest Data using Python Script

Use the ingest_data.py script to load data into the PostgreSQL database.
Example Command:

```commandline
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

## 5. Building and Running a Custom Docker Image for Data Ingestion
Build the Docker Image

```commandline
docker build -t taxi_ingest:v001 .
```
Ingest Yellow Taxi Trip Data

```commandline
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-09.csv.gz"
docker run -it \
    --rm \
    --network=de-zoomcamp-2024-wk-1_default \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=de-zoomcamp-2024-wk-1-pg-database-1 \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
```
Ingest Taxi Zone Data

```commandline
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
docker run -it \
    --rm \
    --network=de-zoomcamp-2024-wk-1_default \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=de-zoomcamp-2024-wk-1-pg-database-1 \
        --port=5432 \
        --db=ny_taxi \
        --table_name=zones \
        --url=${URL}
```

You may need to use docker commands ps and docker network commands list to find the actual names of your network and container names

## 6. Terraform Commands

```commandline
Init
```

```commandline
Plan
```

```commandline
Apply
```

```commandline
Destroy
```

## 7. Google Cloud VM Instance

- https://cloud.google.com/compute/docs/connect/create-ssh-keys
- Create SSH key in /ssh folder using command from documentation above
- Go to Compute Engine/meta data and add public key


wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh
bash Anaconda3


