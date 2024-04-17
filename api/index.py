import os
import secrets
import sys
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import psycopg2
from api.database import authenticate_user,  initialize_database
from api.traindb import initialize_traindatabase
app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16)
comments = []
initialize_database()
initialize_traindatabase()
# Route for handling login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = authenticate_user(username, password)
    session['username'] = username
    if user:
        # Authentication successful, redirect to home page
        return redirect(url_for('home'))
    else:
        error_message = "Incorrect username or password"
        session['error_message'] = error_message
        return redirect(url_for('login_page'))

# Route for login page
@app.route('/')
def login_page():
    error_message = session.pop('error_message', None)
    return render_template('login.html', error_message=error_message)

@app.route('/home')
def home():
    username = session.get('username')
    return render_template('home.html', username=username, comments=comments)
# Route for handling search
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", "5432"),  # Default port is 5432
        sslmode=os.getenv("POSTGRES_SSLMODE", "require")  # Default SSL mode is require
    )
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Use psycopg2's mogrify function to safely format the query parameters
        query = '%' + query + '%'
        cursor.execute("SELECT * FROM trains WHERE name LIKE %s OR number LIKE %s", (query, query))
        
        # Fetch all rows from the query result
        search_results = cursor.fetchall()
        
        # Close the database connection
        conn.close()
        
        # Convert search results to JSON format
        results_json = [{'name': row[1], 'number': row[2], 'source': row[3], 'destination': row[4]} for row in search_results]
        
        return jsonify(results_json)
    
    except psycopg2.Error as e:
        # Handle any database errors
        return jsonify({'error': str(e)})


@app.route('/add_comment', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        # Get the comment data from the form
        comment = request.form['comment']
        
        # Append the comment to the list
        comments.append(comment)
        
        # Redirect back to the main page after adding the comment
        return redirect(url_for('home'))

@app.route('/logout', methods=['POST'])
def logout():
    # Clear the session
    session.clear()
    # Redirect to the login page
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
