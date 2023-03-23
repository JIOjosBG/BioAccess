from machine import Pin, UART
import time

touch_out = Pin(22, Pin.IN)
tx_pin = Pin(0, Pin.OUT)
rx_pin = Pin(1, Pin.IN)
uart = UART(0, 11520)
uart.init(11520, bits=8, parity=None, stop=1, tx=tx_pin, rx=rx_pin)

cmd = b'\xF5\xC3\x03\x07\x96\x00\x51\xF5'#'F5 C3 03 07 96 00 51 F5'
print(cmd)
uart.write(bytearray(cmd))
