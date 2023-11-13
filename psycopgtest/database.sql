CREATE TABLE RuuviSensorData (
    id SERIAL PRIMARY KEY,
    uuid VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    temperature DECIMAL(5, 2) NOT NULL,
    humidity DECIMAL(5, 2) NOT NULL,
    pressure DECIMAL(7, 2) NOT NULL,
    acceleration_x DECIMAL(7, 4) NOT NULL,
    acceleration_y DECIMAL(7, 4) NOT NULL,
    acceleration_z DECIMAL(7, 4) NOT NULL,
    battery_voltage DECIMAL(6, 3) NOT NULL,
    tx_power INT NOT NULL,
    movement_counter INT NOT NULL,
    measurement_sequence INT NOT NULL
);