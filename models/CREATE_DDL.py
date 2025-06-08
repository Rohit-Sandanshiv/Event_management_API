import sqlite3
import os
from db_connection import get_db_connection


conn = get_db_connection()
cursor = conn.cursor()


# to ensure foreign key works
cursor.execute("PRAGMA foreign_keys = ON;")


cursor.execute('DROP TABLE IF EXISTS events')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(
    id TEXT PRIMARY KEY,
    name TEXT,
    location TEXT,
    start_time DATETIME,
    end_time DATETIME,
    max_capacity INT
);
""")

cursor.execute('DROP TABLE IF EXISTS attendees')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendees(
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    event_id TEXT,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);
""")

print("✅ Database and tables created successfully!")
print("✅ Tables created successfully in MEMS_DB")


conn.commit()
conn.close()