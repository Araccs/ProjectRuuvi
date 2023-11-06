import asyncio
import bleak


async def scan_for_devices():
    devices = await bleak.discover()
    return devices

# Run the scan
loop = asyncio.get_event_loop()
nearby_devices = loop.run_until_complete(scan_for_devices())

for device in nearby_devices:
    print(f"Device name: {device.name}")
    print(f"Device address: {device.address}")
    print(f"Advertising data: {device.metadata['manufacturer_data']}")


    