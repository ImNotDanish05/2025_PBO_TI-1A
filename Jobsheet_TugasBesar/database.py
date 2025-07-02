import sqlite3
import pandas as pd
from config import DB_PATH

# Mencari Koneksi ke database SQLite
# Jika tidak ada, akan mengembalikan None
def get_db_connection() -> sqlite3.Connection | None:
    """Create a database connection to the SQLite database specified by DB_PATH."""
    try:
        conn = sqlite3.connect(
            DB_PATH,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            timeout=10  # Wait up to 10 seconds for the database lock to clear
        )
        conn.row_factory = sqlite3.Row  # Supaya akses kolom pakai nama
        return conn
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Koneksi DB gagal: {e}")
        return None

# Eksekusi seperti CRUD: INSERT, UPDATE, DELETE
def execute_query(query: str, params: tuple = ()) -> bool:
    """Execute a single SQL query."""
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        if query.strip().upper().startswith("INSERT"):
            return cursor.lastrowid
        return True
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Gagal eksekusi query: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

# Eksekusi query yang mengembalikan data, seperti SELECT
def fetch_query(query: str, params: tuple = None, fetch_all: bool = True):
    """
    Menjalankan query SELECT dan mengembalikan hasil:
    - fetch_all=True: list of rows
    - fetch_all=False: single row
    """
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        result = cursor.fetchall() if fetch_all else cursor.fetchone()
        return result
    except sqlite3.Error as e:
        print(f"ERROR [database.py] Fetch gagal: {e} | Query: {query[:60]}")
        return None
    finally:
        if conn:
            conn.close()

# Eksekusi query SELECT dan mengembalikan hasil sebagai DataFrame Pandas
def get_dataframe(query: str, params: tuple = None) -> pd.DataFrame:
    """Menjalankan query SELECT dan mengembalikan hasil sebagai DataFrame Pandas."""
    conn = get_db_connection()
    if not conn:
        return pd.DataFrame()

    try:
        df = pd.read_sql_query(query, conn, params=params)
        return df
    except Exception as e:
        print(f"ERROR [database.py] Gagal baca ke DataFrame: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Setup awal database, bikin tabel jika belum ada
# Fungsi ini menjadi auto setup saat pertama kali dijalankan
def setup_database_initial():
    print(f"Memeriksa/membuat tabel di database (via database.py): {DB_PATH}")
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        sql_create = """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            google_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            name TEXT DEFAULT 'NotName',
            picture TEXT DEFAULT 'https://placehold.co/400x400?text=?',

            token TEXT NOT NULL,
            refresh_token TEXT NOT NULL,
            token_uri TEXT NOT NULL,
            client_id TEXT NOT NULL,
            client_secret TEXT NOT NULL,
            scopes TEXT NOT NULL,
            expiry TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS channel (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            channel_id TEXT NOT NULL UNIQUE,
            title TEXT DEFAULT 'Unknown',
            subscribers INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1,

            FOREIGN KEY(user_id) REFERENCES user(id)
        );

        CREATE TABLE IF NOT EXISTS video (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT NOT NULL,
            video_id TEXT NOT NULL UNIQUE,
            title TEXT DEFAULT 'Unknown',
            description TEXT,
            published_at TEXT,
            comment_count INTEGER DEFAULT 0,
            FOREIGN KEY(channel_id) REFERENCES channel(channel_id)
        );

        CREATE TABLE IF NOT EXISTS comment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            comment_id TEXT NOT NULL UNIQUE,
            author TEXT,
            comment TEXT NOT NULL,
            published_at TEXT,
            FOREIGN KEY(video_id) REFERENCES video(video_id)
        );

        """
        cursor.executescript(sql_create)
        conn.commit()
        print("-> Semua tabel siap.")
        return True
    except sqlite3.Error as e:
        print(f"Error SQLite saat setup tabel: {e}")
        return False
    finally:
        if conn:
            conn.close()
