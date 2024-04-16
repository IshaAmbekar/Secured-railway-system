import os
import psycopg2
from psycopg2 import sql

def authenticate_user(username, password):
    # Connect to PostgreSQL database using environment variables
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", "5432"),  # Default port is 5432
        sslmode=os.getenv("POSTGRES_SSLMODE", "require")  # Default SSL mode is require
    )
    cursor = conn.cursor()

    # Execute SQL query to authenticate user
    query = sql.SQL("SELECT * FROM users WHERE username = %s AND password = %s")
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    # Close database connection
    cursor.close()
    conn.close()

    return user

def initialize_database():
    # Connect to PostgreSQL database using environment variables
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", "5432"),  # Default port is 5432
        sslmode=os.getenv("POSTGRES_SSLMODE", "require")  # Default SSL mode is require
    )
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    ''')

    # Check if there are any users in the table
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]

    if count == 0:
        # If no users exist, insert initial data
        user_data = [
            ('user1', 'password1'),
            ('user2', 'password2'),
            ('user3', 'password3')
        ]
        cursor.executemany('INSERT INTO users (username, password) VALUES (%s, %s)', user_data)

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Call the function to initialize the database when this script is run directly
if __name__ == '__main__':
    initialize_database()
