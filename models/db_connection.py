import os
import sqlite3


# Ensure database connection is always open when needed
def get_db_connection():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "MEMS.db")
    return sqlite3.connect(db_path, check_same_thread=False)