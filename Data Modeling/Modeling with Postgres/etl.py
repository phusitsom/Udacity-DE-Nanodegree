import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Process json file of song data and insert into artist and song table

    Args:
        cur (psycopg2.extensions.cursor): cursor object
        filepath (str): path to json file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    for i, row in df.iterrows():
        # insert artist record
        artist_data = row[['artist_id', 'artist_name', 'artist_location', 
                            'artist_latitude', 'artist_longitude']].values
        cur.execute(artist_table_insert, artist_data)

        # insert song record
        song_data = row[['song_id', 'title', 
                         'artist_id', 'year', 'duration']].values
        cur.execute(song_table_insert, song_data)

def process_log_file(cur, filepath):
    """Process json file of log data and insert into time, users and songplay table

    Args:
        cur (psycopg2.extensions.cursor): _description_
        filepath (str): _description_
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong'].astype({'ts': 'datetime64[ms]'})

    # convert timestamp column to datetime
    t = df['ts']
    
    # insert time data records
    time_data = [[v, v.hour, v.day, v.week, v.month, v.year, v.day_name()] for v in t]
    column_labels = ("timestamp", "hour", "day", "weelofyear", "month", "year", "weekday")
    time_df = pd.DataFrame.from_records(time_data, columns = column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """Find json files in filepath and process them with the relevant function

    Args:
        cur (psycopg2.extensions.cursor): cursor object
        conn (psycopg2.extensions.connection): connection object
        filepath (str): path to json files
        func (callable): function to process json files
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()