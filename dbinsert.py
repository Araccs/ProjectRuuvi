from flask import Flask, request
import psycopg2
import json

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

def insert_into_database(data):
    # Extract the UUID and JSON data from the received data
    sensor_data = json.dumps({'sensordata': data})

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="sensordata",
        user="postgres",
        password="abomination",
        host="localhost",
        port="5432"
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # SQL query to insert data into RuuviSensorData table
    insert_query = """
        INSERT INTO sensordata (sensordata)
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

if __name__ == '__main__':
    app.run(debug=True)
