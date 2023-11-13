import psycopg2
from datetime import datetime

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

# Data to be inserted
data = (
    "3add7302-a93d-4297-89f2-8e07922c6730",
    datetime.now(),
    25.5,
    50.0,
    1013.25,
    0.0,
    0.0,
    0.0,
    3.0,
    10,  # Replace with the appropriate value for tx_power
    5,   # Replace with the appropriate value for movement_counter
    1    # Replace with the appropriate value for measurement_sequence
)

# Execute the SQL query with the data
cur.execute(insert_query, data)

# Commit the transaction
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()