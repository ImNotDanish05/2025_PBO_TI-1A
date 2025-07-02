import sqlite3
import os
from config import DB_PATH

def create_database():
    # Ensure the directory exists
    print(f"Creating database at {DB_PATH}")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = None
    try:
        # Connect to the SQLite database (it will be created if it doesn't exist)
        conn = sqlite3.connect(DB_PATH)
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Create a table if it doesn't exist
        sql_code = """
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
        
        cursor.executescript(sql_code)
        # Commit the changes and close the connection
        conn.commit()
        print("Database and tables created successfully.")
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        if conn:
            conn.close()
        return False
    finally:
        if conn:
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    # Run the function to create the database
    if create_database():
        print("✅ Database setup complete!")
    else:
        print("❌ Database setup failed.")