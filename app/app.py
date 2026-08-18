import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "demo")
DB_USER = os.getenv("DB_USER", "demo")
DB_PASSWORD = os.getenv("DB_PASSWORD", "demo")


@app.get("/")
def root():
    return {"message": "Hello from Kubernetes"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/db")
def database_check():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return {
            "database": "connected",
            "version": result[0]
        }

    except Exception as e:
        return {
            "database": "connection failed",
            "error": str(e)
        }