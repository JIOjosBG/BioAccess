from machine import Pin, UART
import time

ACK_SUCCESS = 0x00 #execution succeed
ACK_FAIL = 0x01 #Execution failed
ACK_FULL = 0x04 #database is full
ACK_NOUSER = 0x05 #No such user
ACK_USER_EXIST = 0x07 #User already exists
ACK_TIMEOUT = 0x08 #Image capture timeout
ACK_HARDWAREERROR = 0x0A #hardware error
ACK_IMAGEERROR = 0x10 #image error
ACK_BREAK = 0x18 #terminate the current command
ACK_ALGORITHFAIL = 0x11 #Film attack detection
ACK_HOMOLOGYFAIL = 0x12 #homology check error

touch_out = Pin(3, Pin.IN)
uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
uart.init(bits=8, parity=None, stop=1)

def checksum(data):
    return data[1]^data[2]^data[3]^data[4]^data[5] == data[6]
class sfm_v17:
    def __init__(self, uart, touch_out):
        self.uart = uart
        self.touch_out = touch_out
    def register(self):
        #while touch_out.value() == 0:
        #    time.sleep_ms(20)
        self.led_white()
        #first cmd
        self.uart.write(b'\xF5\x01\x00\x00\x00\x00\x01\xF5')
        while True:
            if uart.any():
                data = uart.read(8) # Read up to 10 bytes from UART buffer
                print(data)
                if checksum(data) == 0:
                    self.led_red()
                    return -1
                if data[1] != 1:
                    self.led_red()
                    return -1
                if data[4] != 0:
                    self.led_red()
                    return -1
                break
        #second cmd
        self.uart.write(b'\xF5\x02\x00\x00\x00\x00\x02\xF5')
        while True:
            if uart.any():
                data = uart.read(8) # Read up to 10 bytes from UART buffer
                print(data)
                if checksum(data) == 0:
                    self.led_red()
                    return -1
                if data[1] != 2:
                    self.led_red()
                    return -1
                if data[4] != 0:
                    self.led_red()
                    return -1
                break
        #third cmd
        self.uart.write(b'\xF5\x03\x00\x00\x00\x00\x03\xF5')
        while True:
            if uart.any():
                data = uart.read(8) # Read up to 10 bytes from UART buffer
                print(data)
                if checksum(data) == 0:
                    self.led_red()
                    return -1
                if data[4] != 0:
                    self.led_red()
                    return -1
                break
        #return success
        self.led_green()
        return 0
    def verify(self):
        #while touch_out.value() == 0:
        #    time.sleep_ms(20)
        self.led_white()
        self.uart.write(b'\xF5\x0C\x00\x00\x00\x00\x0C\xF5')
        while True:
            if uart.any():
                data = uart.read(8)
                print(data)
                if data == b'\xF5\x0C\x00\x00\x00\x00\x0C\xF5':
                    self.led_red()
                    return -1
                if checksum(data) == 0:
                    self.led_red()
                    return -1
                break
        self.led_green()
        return 0
    def led_red(self):
        self.uart.write(b'\xF5\xC3\x03\x03\x96\x00\x55\xF5')
        while True:
            if uart.any():
                data = uart.read(8)
                if checksum(data) == 0:
                    return -1
                break
        return 0
    def led_green(self):
        self.uart.write(b'\xF5\xC3\x05\x05\x96\x00\x55\xF5')
        while True:
            if uart.any():
                data = uart.read(8)
                if checksum(data) == 0:
                    return -1
                break
        return 0
    def led_white(self):
        self.uart.write(b'\xF5\xC3\x00\x00\x96\x00\x55\xF5')
        while True:
            if uart.any():
                data = uart.read(8)
                if checksum(data) == 0:
                    return -1
                break
        return 0
    def led_off(self):
        self.uart.write(b'\xF5\xC3\x07\x07\x96\x00\x55\xF5')
        while True:
            if uart.any():
                data = uart.read(8)
                if checksum(data) == 0:
                    return -1
                break
        return 0
    def delete_all(self):
        self.uart.write(b'\xF5\x05\x00\x00\x00\x00\x05\xF5')
        while True:
            if uart.any():
                data = uart.read(8)
                if checksum(data) == 0:
                    return -1
                if data != b'\xF5\x05\x00\x00\x00\x00\x05\xF5':
                    return -1
                break
        return 0


'''
while True:
    time.sleep_ms(20)
    print(touch_out.value())
'''
sensor = sfm_v17(uart, touch_out)
'''
print(sensor.delete_all())


while True:
    if sensor.delete_all() == 0:
        bre ak
'''
register = 0

while True:
    if register == 1:
        print(sensor.register())
        register = 0
    else:
        print('go')
        print(sensor.verify())
        time.sleep_ms(500)
        sensor.led_off()
'''
if register == 1:
    print(sensor.register())
else:
    print('go')
    print(sensor.verify())
time.sleep(1)
sensor.led_off()

touch_out = Pin(22, Pin.IN)
tx_pin = Pin(0, Pin.OUT)
rx_pin = Pin(1, Pin.IN)
uart = UART(0, 11520)
uart.init(11520, bits=8, parity=None, stop=1, tx=tx_pin, rx=rx_pin)

cmd = b'\xF5\xC3\x03\x07\x96\x00\x51\xF5'#'F5 C3 03 07 96 00 51 F5'
print(cmd)
uart.write(bytearray(cmd))
'''