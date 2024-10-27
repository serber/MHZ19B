# MHZ19B sensor app
MicroPython code to work with MHZ19B sensor via UART

#### Example for Raspberry Pi Pico
```python
mhz19b = MHZ19B(uart_id=1, tx_pin=8, rx_pin=9)
while True:
 co2 = mhz19b.read_co2()
 if co2 is not None:
     print("CO2: ", co2, "ppm")
 else:
     print("Failed to read data from sensor")
time.sleep(2)
```

#### Calibration
In some cases sensor calibration may be required (for example, `read_co2` method always return 5000 ppm)
> Calibration should be performed outdoors

Use `calibrate` method for that (only once)
```python
mhz19b = MHZ19B(uart_id=1, tx_pin=8, rx_pin=9)
mhz19b.calibrate(led_pin=25)
```