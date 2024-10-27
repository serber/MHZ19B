# Class for reading data from MHZ19B sensor
#
# 2024-10-27 21:58:22
#
# Usage:
# mhz19b = MHZ19B(uart_id=1, tx_pin=8, rx_pin=9)
# while True:
#     co2 = mhz19b.read_co2()
#     if co2 is not None:
#         print("CO2 Concentration:", co2, "ppm")
#     else:
#         print("Failed to read data from sensor")
#     time.sleep(2)

import machine
import time

class MHZ19B:
    def __init__(self, uart_id, tx_pin, rx_pin, baudrate=9600):
        self.uart = machine.UART(uart_id, baudrate=baudrate, tx=tx_pin, rx=rx_pin)

    def read_co2(self):
        request = bytearray([0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79])
        self.uart.write(request)
        
        time.sleep(0.1)

        if self.uart.any():
            response = self.uart.read(9)
            if self.validate_response(response):
                return response[2] * 256 + response[3]
        return None
    
    def calibrate(self, led_pin):
        led = machine.Pin(led_pin, machine.Pin.OUT)

        print("Please wait for 20 minutes in clean air")

        for _ in range(11):
            led.toggle()
            time.sleep(0.5)

        print("Waiting 20 minutes")

        time.sleep(1200)

        print("Starting calibration")

        request = bytearray([0xFF, 0x01, 0x87, 0x00, 0x00, 0x00, 0x00, 0x00, 0x78])
        self.uart.write(request)

        print("Calibration command sent")
        
        return

    def validate_response(self, response):
        if len(response) != 9 or response[0] != 0xFF or response[1] != 0x86:
            return False
        
        # Sum bytes from index 1 to 7 and compare with last byte
        checksum = sum(response[1:8]) & 0xFF
        if checksum == response[8]:
            return True
        
        return False