
# Data Modeling with Postgres

## **Overview**
In this project, I applied the concepts of data modeling to a real-world problem. I built an ETL pipeline to transform the data from a json files (song and logging data) into a postgres database.

## **Song Dataset**
```
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

## **Log Dataset**
```
{"artist": null, "auth": "Logged In", "firstName": "Walter", "gender": "M", "itemInSession": 0, "lastName": "Frye", "length": null, "level": "free", "location": "San Francisco-Oakland-Hayward, CA", "method": "GET","page": "Home", "registration": 1540919166796.0, "sessionId": 38, "song": null, "status": 200, "ts": 1541105830796, "userAgent": "\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"", "userId": "39"}
```


## Schema

#### Fact Table 
**songplays** - records in log data associated with song plays i.e. records with page `NextSong`

```
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
```

#### Dimension Tables
**users**  - users in the app
```
user_id, first_name, last_name, gender, level
```
**songs**  - songs in music database
```
song_id, title, artist_id, year, duration
```
**artists**  - artists in music database
```
artist_id, name, location, latitude, longitude
```
**time**  - timestamps of records in  **songplays**  broken down into specific units
```
start_time, hour, day, week, month, year, weekday
```

## Project Files

```sql_queries.py``` contains SQL queries for inseting, dropping and creating tables.

```create_tables.py```. Running this file creates **sparkifydb** database and the tables.

```etl.ipynb``` is a jupyter notebook to test and analyze the dataset before loading. 

```etl.py``` is a python file for processing **song_data** and **log_data**.

```test.ipynb``` is a notebook to connect to postgres database and validate that the data is loaded.

## How to run
1. Create and initialize the `sparkifydb` database by running `create_tables.py`
```
python create_tables.py
```
2. Insert data into the database by running `etl.py`
```
python etl.py
```