import sys
import ubinascii

__version__ = b'0.1.0'


try:
    import machine
    unique_id =  ubinascii.hexlify(machine.unique_id())
except:
    #This can happen in UNIX mode
    unique_id = "set-a-unique-device-id"

try:
    import network
    local_ip = bytes(network.WLAN(0).ifconfig()[0], 'utf-8')
except:
    local_ip = "127.0.0.1"

try:
    import network
    local_mac = ubinascii.hexlify(network.WLAN(0).config('mac'), ':')
except:
    local_mac = "cannotgetlocalmac"



# Default config
CONFIG = {
    'mqtt': {
        'broker': '127.0.0.1',
        'port': 0,
        'user': None,
        'pass': None,
        'keepalive': 60,
        'ssl': False,
        'ssl_params': {},
        'base_topic': b'homie'
    },
    'device': {
        'id': unique_id,
        'name': b'mydevice',
        'fwname': b'uhomie',
        'fwversion': __version__,
        'localip': local_ip,
        'mac': local_mac,
        'platform': bytes(sys.platform, 'utf-8'),
        'stats_interval': 60
    }
}