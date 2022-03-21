from decouple import RepositoryIni, Config

config = Config(RepositoryIni("settings.ini"))


CLIENT_ID=config("CLIENT_ID")
CLIENT_SECRET=config("CLIENT_SECRET")
DB_CONNSTR=config("DB_CONNSTR")
SPOTIPY_REDIRECT_URI=config("SPOTIPY_REDIRECT_URI")

print(DB_CONNSTR)