from flask import Flask, render_template, request
import psycopg2
import json
from config import DATABASE_CONFIG

app = Flask(__name__)

# Route to receive data from your sensor
@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()

    # Print the received data for debugging
    print("Received Data:", data)

    # Insert the data into the PostgreSQL database
    insert_into_database(data)

    return "Data received and stored successfully"

@app.route('/show_data')
def show_data():
    data = get_data_from_database()
    return render_template('show_data.html', data=data)

def insert_into_database(data):
    # Extract the UUID and JSON data from the received data
    sensor_data = json.dumps({'sensordata': data})

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**DATABASE_CONFIG)

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # SQL query to insert data into RuuviSensorData table
    insert_query = """
        INSERT INTO sensordatatable (sensorresult)
        VALUES (%s)
    """
    print("Sensor Data:", sensor_data)
    # Execute the SQL query with the UUID and JSON data
    cur.execute(insert_query, (sensor_data,))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

def get_data_from_database():
    conn = psycopg2.connect(**DATABASE_CONFIG)
    cur = conn.cursor()
    select_query = "SELECT data_id, sensorresult FROM sensordatatable"
    cur.execute(select_query)
    data = cur.fetchall()
    print(data)
    cur.close()
    conn.close()
    return data


@app.route('/search', methods=['GET', 'POST'])
def search_data():
    if request.method == 'POST':
        search_query = request.form.get('search_query')

        # Connect to the database
        conn = psycopg2.connect(**DATABASE_CONFIG)
        cur = conn.cursor()

        # Example: Search by UUID
        query = f"SELECT * FROM sensordatatable WHERE sensorresult->>'Temperature' LIKE '{search_query}%'"
        cur.execute(query)
        result = cur.fetchall()

        # You can customize the query based on your data model and search criteria
        print("Search Query:", query)
        print("Result:", result)
        # Close the cursor and connection
        cur.close()
        conn.close()

        return render_template('search_results.html', results=result)

    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)