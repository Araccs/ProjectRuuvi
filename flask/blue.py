import asyncio
import bleak
import struct
import json
import requests

async def scan_for_devices_and_parse():
    while True:
        devices = await bleak.discover()
        
        for device in devices:
            manufacturer_data = device.metadata.get('manufacturer_data', {})
            
            if 1177 in manufacturer_data:
                data = manufacturer_data[1177]
                
                if len(data) == 24:
                    # Parse the data based on the RAWv2 format
                    temperature, humidity, pressure, acceleration_x, acceleration_y, acceleration_z, battery_voltage, tx_power = struct.unpack('!hHIBBBHB', data[:14])
                    
                    # Convert the raw values to actual sensor readings
                    temperature = struct.unpack('!h', data[1:3])[0] * 0.005
                    humidity = struct.unpack('!H', data[3:5])[0] * 0.0025
                    pressure = struct.unpack('!H', data[5:7])[0] + 50000
                    pressure_hpa = pressure / 100.0
                    acceleration_x = struct.unpack('!h', data[7:9])[0] / 1000.0
                    acceleration_y = struct.unpack('!h', data[9:11])[0] / 1000.0
                    acceleration_z = struct.unpack('!h', data[11:13])[0] / 1000.0
                    battery_voltage = (struct.unpack('!H', data[13:15])[0] * 1.0) + 1600
                    battery_voltage = battery_voltage / 100
                    tx_power = struct.unpack('!B', data[15:16])[0]
                    
                    # Create a dictionary with the parsed data
                    parsed_data = {
                        "Temperature": round(temperature, 2),
                        "Humidity": round(humidity, 2),
                        "Pressure": round(pressure_hpa, 2),
                        "Acceleration (X, Y, Z)": (round(acceleration_x, 2), round(acceleration_y, 2), round(acceleration_z, 2)),
                        "Battery Voltage": round(battery_voltage, 2),
                        "TX Power": tx_power
                    }
                    
                    # Print the parsed data
                    print(json.dumps(parsed_data, indent=4))

                    # Send the parsed data to the Flask web application
                    response = requests.post('http://127.0.0.1:5000/receive_data', json=parsed_data)
                    if response.status_code == 200:
                        print("Data sent to Flask successfully")
                    else:
                        print("Failed to send data to Flask")
                else:
                    print("Invalid data length")

# Run the continuous scan and parsing
loop = asyncio.get_event_loop()
loop.run_until_complete(scan_for_devices_and_parse())