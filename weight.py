import bluetooth
import pygatt

# The BGAPI backend will attempt to auto-discover the serial device name of the
# attached BGAPI-compatible USB adapter.
adapter = pygatt.BGAPIBackend()

target_name = "weight"
target_characteristic = "a1e8f5b1-696b-4e4c-87c6-69dfe0b0093b"
target_value = bytearray([0, 1, 2])
target_addresses = []

print("Looking for target name %s" % target_name)

nearby_devices = bluetooth.discover_devices(lookup_names=True)

for bdaddr, name in nearby_devices:
    print("Found %s - %s" % (bdaddr, name))
    if target_name == name:
        target_addresses.append(bdaddr)

if target_addresses:
    for target_address in target_addresses:
        print("Found target bluetooth device with address ", target_address)
    try:
        adapter.start()
        for target_address in target_addresses:
            print("Writing to ", target_address)
            device = adapter.connect(target_address)
            device.char_write(target_characteristic, target_value)
            adapter.disconnect()
    finally:
        adapter.stop()
else:
    print("Could not find target bluetooth device nearby")


