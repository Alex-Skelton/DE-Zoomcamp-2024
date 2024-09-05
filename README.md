# DE-Zoomcamp 2024 - Week 1
This README servers as my course notes when running commands on Ubuntu for me and others students to refer back to.

Ensuring Docker is installed:

```console
docker --version
```

## 1. Running Python in Docker
Start a Python Docker container

Run a Python container interactively (-it):

```bash
docker run -it python:3.11
```
Start a Python container with Bash (for pip and other commands..):

```bash
docker run -it --entrypoint bash python:3.11
```

## 2. Useful Docker Commands
List running Docker containers
```bash
docker ps
```
List Docker networks
```bash
docker network ls
```

Inspect a Docker network

Replace {name} with the name of the network:

```bash
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

```bash
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

```bash
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
 ```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz"
```
Taxi Zone Lookup Table:
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
```
Ingest Data using Python Script

Use the ingest_data.py script to load data into the PostgreSQL database.
Example Command:

```bash
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

```bash
docker build -t taxi_ingest:v001 .
```
Ingest Yellow Taxi Trip Data

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2019-01.csv.gz"
docker run -it \
    --rm \
    --network=de-zoomcamp-2024-week-1_default \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=de-zoomcamp-2024-week-1-pg-database-1 \
        --port=5432 \
        --db=ny_taxi \
        --table_name=yellow_taxi_trips \
        --url=${URL}
```
Ingest Taxi Zone Data

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"
docker run -it \
    --rm \
    --network=de-zoomcamp-2024-week-1_default \
    taxi_ingest:v001 \
        --user=root \
        --password=root \
        --host=de-zoomcamp-2024-week-1-pg-database-1 \
        --port=5432 \
        --db=ny_taxi \
        --table_name=zones \
        --url=${URL}
```

You may need to use docker commands ps and docker network commands list to find the actual names of your network and container names