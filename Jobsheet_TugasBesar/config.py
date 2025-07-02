import os

BASE_DIR = "database"
NAMA_DB = 'DB_Youtube.db'
DB_PATH = os.path.join(BASE_DIR, NAMA_DB)
LOGIN_SESSION = "login_session.csv"

# Lokasi file
CREDENTIALS_PATH = 'database/credentials.json'

# Scope yang dibutuhkan
SCOPES = [
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile"
]

# Loggin Session
TIME_SESSION = 60 # In Minutes

# Setting
DB_COMMENT_DELETEAFTERFINISHEXECUTE = True