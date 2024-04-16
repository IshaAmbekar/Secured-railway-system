import os
import psycopg2
from psycopg2 import sql

def initialize_traindatabase():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", "5432"),  # Default port is 5432
        sslmode=os.getenv("POSTGRES_SSLMODE", "require")  # Default SSL mode is require
    )
    cursor = conn.cursor()
    
    # Create trains table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS trains (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        number TEXT NOT NULL,
                        source TEXT NOT NULL,
                        destination TEXT NOT NULL
                    )''')
    
    # Check if the trains table is empty
    cursor.execute("SELECT COUNT(*) FROM trains")
    row_count = cursor.fetchone()[0]
    
    # If the table is empty, insert sample data into the trains table
    if row_count == 0:
        cursor.execute("INSERT INTO trains (name, number, source, destination) VALUES (%s, %s, %s, %s)",
                       ('Express Train', '12345', 'City A', 'City B'))
        cursor.execute("INSERT INTO trains (name, number, source, destination) VALUES (%s, %s, %s, %s)",
                       ('Local Train', '67890', 'City C', 'City D'))
        conn.commit()

    conn.close()

# Call the initialize_traindatabase() function to ensure that the database is initialized properly
if __name__ == '__main__':
    initialize_traindatabase()
