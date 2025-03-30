import os
import asyncio
import psycopg2


# self.db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"


# Database connection details
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = "db"  # matches the 'services:' name in 'docker-compose.yml'
DB_PORT = "5432"

try:
    # Connect to the database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    
    # Test query
    cur.execute("SELECT version();")
    print("PostgreSQL version:", cur.fetchone())

    # Close connection
    cur.close()
    conn.close()
except Exception as e:
    print("Error:", e)
