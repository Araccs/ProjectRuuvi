from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

app = Flask(__name__)

# Configure the Flask application to use PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:purki5ujoV@localhost/RuuviSensorData'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class RuuviSensorData(db.Model):
    __tablename__ = 'RuuviSensorData'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    temperature = db.Column(db.DECIMAL(5, 2), nullable=False)
    humidity = db.Column(db.DECIMAL(5, 2), nullable=False)
    pressure = db.Column(db.DECIMAL(7, 2), nullable=False)
    acceleration_x = db.Column(db.DECIMAL(7, 4), nullable=False)
    acceleration_y = db.Column(db.DECIMAL(7, 4), nullable=False)
    acceleration_z = db.Column(db.DECIMAL(7, 4), nullable=False)
    battery_voltage = db.Column(db.DECIMAL(6, 3), nullable=False)
    tx_power = db.Column(db.Integer, nullable=False)
    movement_counter = db.Column(db.Integer, nullable=True)
    measurement_sequence = db.Column(db.Integer, nullable=True)

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
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname="RuuviSensorData",
        user="postgres",
        password="purki5ujoV",
        host="localhost",
        port="5432"
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    # SQL query to insert data into RuuviSensorData table
    insert_query = """
        INSERT INTO RuuviSensorData (
            uuid, timestamp, temperature, humidity, pressure, 
            acceleration_x, acceleration_y, acceleration_z, 
            battery_voltage, tx_power, movement_counter, measurement_sequence
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Extract values from the data dictionary
    values = (
        data.get('UUID', ''),
        datetime.strptime(data.get('Timestamp', ''), '%Y-%m-%dT%H:%M:%S.%f%z') if 'Timestamp' in data else None,
        data.get('Temperature', None),
        data.get('Humidity', None),
        data.get('Pressure', None),
        data.get('Acceleration (X, Y, Z)', (None, None, None))[0],
        data.get('Acceleration (X, Y, Z)', (None, None, None))[1],
        data.get('Acceleration (X, Y, Z)', (None, None, None))[2],
        data.get('Battery Voltage', None),
        data.get('TX Power', None),
        data.get('Movement Counter', 0),
        data.get('Measurement Sequence', 0)
    )

    # Execute the SQL query with the data
    cur.execute(insert_query, values)

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)
