CREATE DATABASE ruuvitietokanta;
USE ruuvitietokanta;
CREATE TABLE ruuvitietokanta (id int NOT NULL AUTO_INCREMENT, temperature NUMERIC, pressure NUMERIC, humidity NUMERIC, Battery_Voltage NUMERIC, TX_Power NUMERIC, PRIMARY KEY (id);
