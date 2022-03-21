from curses import raw
from distutils.command.clean import clean
from http import client
from shutil import ExecError
from cfg import CLIENT_ID, CLIENT_SECRET, DB_CONNSTR, SPOTIPY_REDIRECT_URI
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
from models import TABLENAME
import pandas as pd
from sqlalchemy import create_engine


scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                                scope=scope))



def extract(date, limit=50) -> list:
    """
    Get limited elements from last listen tracks on spotify

    Args:
        date(datetime): Date to query
        limit(int): Limit of elements to query

    Returns:

    """

    ds = int(date.timestamp()) * 1000
    return sp.current_user_recently_played(limit=limit, after=ds)


def transform(raw_data, date):
    """
    Process raw data and clean it

    Args: 
        raw_data(dict): dict with the raw data to process
        date(datetime): Date of the raw data extraction

    Returns:
        df(): Processed dataframe
    """
    listen_tracks = []
    for data in raw_data["items"]:
        listen_tracks.append(
            {
                "played_at": data["played_at"],
                "artist": data["track"]["artists"][0]["name"],
                "track": data["track"]["name"]
            }
        )
    df = pd.DataFrame(listen_tracks)

    #Removing dates differents from what we want to have
    clean_df = df[pd.to_datetime(df["played_at"]).dt.date == date.date()]

    #Data validation
    if not df["played_at"].is_unique:
        raise Exception("A value from played at is not unique")

    if df.isnull().values.any():
        raise Exception("A value from df is null")
    
    #return clean_df
    return clean_df


def load(df):
    """
    Load the clean data to database previusly configurated

    Args: 
        - df (pd.Dataframe): A dataframe with clean data ready to be uploaded to some database
    """
    print(f"Uploading {df.shape[0]} to Postgresql database")
    engine = create_engine(DB_CONNSTR)
    df.to_sql(TABLENAME, con=engine, index=False, if_exists='append')

if __name__ == '__main__':

    date = datetime.today() - timedelta(days=1)

    #Extract
    raw_data = extract(date)
    #print(f"Extracted: {(raw_data['items'])}")

    #Transform
    clean_data = transform(raw_data, date)
    print(clean_data)

    #Load
    load(clean_data)
