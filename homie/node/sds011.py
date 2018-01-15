"""
Taken form https://github.com/g-sam/polly

Reading format. See http://cl.ly/ekot
0 Header   '\xaa'
1 Command  '\xc0'
2 DATA1    PM2.5 Low byte
3 DATA2    PM2.5 High byte
4 DATA3    PM10 Low byte
5 DATA4    PM10 High byte
6 DATA5    ID byte 1
7 DATA6    ID byte 2
8 Checksum Low byte of sum of DATA bytes
9 Tail     '\xab'





SDS011 -- ESP

TX -- RX
RX -- D4 (TX1)
5v -- 5v
GND -- GND


"""

import machine
import ustruct as struct
import sys
import utime as time
from . import HomieNode


def init_uart(x):
    #uart = machine.UART(x, 9600)
    uart = machine.UART(2, baudrate=9600, rx=16, tx=17, timeout=10)
    uart.init(9600, bits=8, parity=None, stop=1)
    return uart

CMDS = {'SET': b'\x01',
        'GET': b'\x00',
        'DUTYCYCLE': b'\x08',
        'SLEEPWAKE': b'\x06'}


class SDS011(HomieNode):

    def __init__(self, interval=60):
        super(SDS011, self).__init__(interval=interval)
        self.pm25 = 0
        self.pm10 = 0
        self.packet_status = True

    def __str__(self):
        return 'SDS011: PM 2.5 = {}, PM 10 = {}'.format(self.pm25, self.pm10)

    def get_node_id(self):
        return [b'pm25', b'pm10', b'packet_status']

    def get_properties(self):
        return (
            (b'pm25/$type', b'pm25'),
            (b'pm25/$properties', b'concentration'),
            (b'pm25/concentration/$settable', b'false'),
            (b'pm25/concentration/$unit', b'mg/m3'),
            (b'pm25/concentration/$datatype', b'float'),
            (b'pm25/concentration/$format', b'20.0:60'),

            (b'pm10/$type', b'pm10'),
            (b'pm10/$properties', b'concentration'),
            (b'pm10/concentration/$settable', b'false'),
            (b'pm10/concentration/$unit', b'mg/m3'),
            (b'pm10/concentration/$datatype', b'float'),
            (b'pm10/concentration/$format', b'20.0:60'),

            (b'packet_status/$type', b'pm10'),
            (b'packet_status/$properties', b'valid'),
            (b'packet_status/valid/$settable', b'false'),
            (b'packet_status/valid/$unit', b'Boolean'),
            (b'packet_status/valid/$datatype', b'boolean'),
            (b'packet_status/valid/$format', b'20.0:60')
        )


    def get_data(self):
        return (
            (b'pm25/amount', self.pm25),
            (b'pm10/amount', self.pm10),
            (b'packet_status/valid', self.packet_status)
        )

    def make_command(self, cmd, mode, param):
        header = b'\xaa\xb4'
        padding = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff'
        checksum = chr(( ord(cmd) + ord(mode) + ord(param) + 255 + 255) % 256)
        tail = b'\xab'
        return header + cmd + mode + param + padding + bytes(checksum, 'utf8') + tail

    def wake(self):
        uart = init_uart(1)
        cmd = self.make_command(CMDS['SLEEPWAKE'], CMDS['SET'], chr(1))
        print('Sending wake command to sds011:', cmd)
        uart.write(cmd)

    def sleep(self):
        uart = init_uart(1)
        cmd = self.make_command(CMDS['SLEEPWAKE'], CMDS['SET'], chr(0))
        print('Sending sleep command to sds011:', cmd)
        uart.write(cmd)


    def update_data(self, allowed_time=20):
        self.wake()
        uart = init_uart(0)
        start_time = time.ticks_ms()
        delta_time = 0
        while (delta_time <= allowed_time * 1000):
            try:
                header = uart.read(1)
                if header == b'\xaa':
                    command = uart.read(1)
                    if command == b'\xc0':
                        packet = uart.read(8)
                        *data, checksum, tail = struct.unpack("<HHBBBs", packet)

                        #verify packet
                        checksum_OK = checksum == (sum(data) % 256)
                        tail_OK = tail == b'\xab'

                        self.pm25 = data[0]/10.0
                        self.pm10 = data[1]/10.0
                        self.packet_status = 'OK' if (checksum_OK and tail_OK) else 'NOK'

                    elif command == b'\xc5':
                        packet = uart.read(8)
                        print('Reply received:', packet)
                delta_time = time.ticks_diff(time.ticks_ms(), start_time) if allowed_time else 0
            except Exception as e:
                print('Problem attempting to read:', e)
                sys.print_exception(e)
        self.sleep()
