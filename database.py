import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connection():
    try:
        con = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            sslmode="require"
        )
        return con

    except Exception as e:
        print("Database Connection Error:", e)
        return None


def get_connection():
    conn = connection()

    if conn is None:
        raise Exception("Database Connection Failed")

    return conn
    