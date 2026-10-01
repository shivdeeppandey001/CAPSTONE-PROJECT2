import sqlite3
import pandas as pd

DATABASE = "database/student_performance.db"

def create_database(df: pd.DataFrame):
    conn = sqlite3.connect(DATABASE)
    df.to_sql("students", conn, if_exists="replace", index=False)
    conn.close()

def get_students():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df
