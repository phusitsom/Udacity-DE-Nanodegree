# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays(
    songplay_id SERIAL PRIMARY KEY,
    start_time TIMESTAMP REFERENCES time (start_time),
    user_id INT REFERENCES users (user_id),
    level VARCHAR NOT NULL,
    song_id VARCHAR(18) REFERENCES songs (song_id),
    artist_id VARCHAR(18) REFERENCES artists (artist_id),
    session_id VARCHAR(18) NOT NULL,
    location TEXT,
    user_agent TEXT
);
                             
""")

user_table_create = ("""CREATE TABLE IF NOT EXISTS users(
    user_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender CHAR(1),
    level VARCHAR NOT NULL
);
""")

song_table_create = ("""CREATE TABLE IF NOT EXISTS songs(
    song_id VARCHAR(18) PRIMARY KEY,
    title TEXT NOT NULL,
    artist_id VARCHAR(18) NOT NULL REFERENCES artists,
    year INT CHECK (year >= 0),
    duration FLOAT
);
""")

artist_table_create = ("""CREATE TABLE IF NOT EXISTS artists(
    artist_id VARCHAR(18) PRIMARY KEY,
    name TEXT,
    location TEXT,
    latitude DECIMAL(8,6),
    longtitude DECIMAL(9,6)  
);
""")

time_table_create = ("""CREATE TABLE IF NOT EXISTS time(
    start_time TIMESTAMP PRIMARY KEY,
    hour INT NOT NULL CHECK (hour >= 0),
    day INT NOT NULL CHECK (day >= 0),
    week INT NOT NULL CHECK (week >= 0),
    month INT NOT NULL CHECK (month >= 0),
    year INT NOT NULL CHECK (year >= 0),
    weekday VARCHAR NOT NULL
);
""")

# INSERT RECORDS

songplay_table_insert = ("""INSERT INTO songplays VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s )
""")

user_table_insert = ("""INSERT INTO users VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level
""")

song_table_insert = ("""INSERT INTO songs VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""INSERT INTO artists VALUES (%s, %s, %s, %s, %s)
                       ON CONFLICT (artist_id) DO UPDATE SET 
                       location = EXCLUDED.location, 
                       latitude = EXCLUDED.latitude, 
                       longtitude = EXCLUDED.longtitude
                       
""")


time_table_insert = ("""INSERT INTO time VALUES (%s, %s, %s, %s, %s, %s, %s)
                     ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""SELECT songs.song_id, artists.artist_id FROM songs 
               JOIN artists ON songs.artist_id = artists.artist_id
               WHERE songs.title = %s AND artists.name = %s AND songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create,
                        song_table_create, time_table_create,
                        songplay_table_create]

drop_table_queries = [songplay_table_drop, user_table_drop,
                      song_table_drop, artist_table_drop, time_table_drop]
