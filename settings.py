import sys
import machine
import network
import ubinascii


# MicroPython Homie implementation version
__version__ = b'0.1.0'


###
# MQTT settings
###

# Broker IP or DNS Name
MQTT_BROKER = '127.0.0.1'

# Broker port
MQTT_PORT = 0

# Username or None for anonymous login
MQTT_USERNAME = None

# Password or None for anonymous login
MQTT_PASSWORD = None

# Defines the mqtt connection timemout in seconds
MQTT_KEEPALIVE = 60

# SSL connection to the broker. Some MicroPython implementations currently
# have problems with receiving mqtt messages over ssl connections.
MQTT_SSL = False
MQTT_SSL_PARAMS = {}

# Base mqtt topic the device publish and subscribes to, without leading slash.
# Base topic format is bytestring
MQTT_BASE_TOPIC = b'homie'


###
# Device settings
###

# The device ID for registration at the broker
DEVICE_ID = ubinascii.hexlify(machine.unique_id())

# Name seen in topic
DEVICE_NAME = b'mydevice'

# Firmware name
DEVICE_FW_NAME = b'uhomie'

# Firmare version
DEVICE_FW_VERSION = __version__

# Local IP from the device
DEVICE_LOCALIP = bytes(network.WLAN(0).ifconfig()[0], 'utf-8')

# Device MAC address
DEVICE_MAC = ubinascii.hexlify(network.WLAN(0).config('mac'), ':')

# Device platform
DEVICE_PLATFORM = bytes(sys.platform, 'utf-8')

# Time in seconds the device updates device properties
DEVICE_STATS_INTERVAL = 60
