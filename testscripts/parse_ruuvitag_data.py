import struct

# Manually input the manufacturer data
manufacturer_data = {1177: b'\x05\x128;\x94\xbb\t\x00\x14\x00\x08\x03\xd4\xb06\xee\x15\xa6\xc6\xf3\xba\x13f?'}






def parse_ruuvitag_data(manufacturer_data):
    if 1177 in manufacturer_data:
        data = manufacturer_data[1177]
        if len(data) == 24:  # The data is 24 bytes long
            # Parse the data based on the RAWv2 format
            temperature, humidity, pressure, acceleration_x, acceleration_y, acceleration_z, battery_voltage, tx_power = struct.unpack('!hHIBBBHB', data[:14])

            # Convert the raw values to actual sensor readings
             # Temperature parsing
            temperature = struct.unpack('!h', data[1:3])[0] * 0.005

            # Humidity parsing
            humidity = struct.unpack('!H', data[3:5])[0] * 0.0025

            # Pressure parsing
            pressure = struct.unpack('!H', data[5:7])[0] + 50000

            pressure_hpa = pressure / 100.0

            # Acceleration parsing
            acceleration_x = struct.unpack('!h', data[7:9])[0] / 1000.0
            acceleration_y = struct.unpack('!h', data[9:11])[0] / 1000.0
            acceleration_z = struct.unpack('!h', data[11:13])[0] / 1000.0

            # Battery voltage parsing
            battery_voltage = (struct.unpack('!H', data[13:15])[0] * 1.0) + 1600  
            battery_voltage = battery_voltage / 100
            # TX power parsing
            tx_power = struct.unpack('!B', data[15:16])[0]

            # Print or use the parsed data
            print(f"Temperature: {temperature:.2f} °C")
            print(f"Humidity: {humidity:.2f} %")
            print(f"Pressure: {pressure_hpa:.2f} hPa")
            print(f"Acceleration (X, Y, Z): ({acceleration_x:.2f}, {acceleration_y:.2f}, {acceleration_z:.2f}) m/s²")
            print(f"Battery Voltage: {battery_voltage:.2f} mV")
            print(f"TX Power: {tx_power} dBm")
            
        else:
            print("Invalid data length")
    else:
        print("Data not found in manufacturer data")

# Call the function with the manually input manufacturer data
parse_ruuvitag_data(manufacturer_data)
