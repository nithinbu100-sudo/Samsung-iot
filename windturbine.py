import RPi.GPIO as GPIO
import time
import board
import busio
import adafruit_dht
import adafruit_bmp280
import spidev

# GPIO Setup
GPIO.setmode(GPIO.BCM)

VIBRATION = 17
BUZZER = 27

GPIO.setup(VIBRATION, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)

# DHT11 Setup
dht = adafruit_dht.DHT11(board.D4)

# BMP280 Setup (I2C)
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

# MCP3008 Setup (SPI)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def buzzer_alert():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(BUZZER, GPIO.LOW)

try:
    while True:
        # Temperature & Humidity
        temperature = dht.temperature
        humidity = dht.humidity

        # Pressure
        pressure = bmp280.pressure

        # Vibration
        vibration = GPIO.input(VIBRATION)

        # Voltage (Channel 0)
        voltage_raw = read_adc(0)
        voltage = (voltage_raw * 3.3) / 1023 * 5  # adjust based on module

        # Current (Channel 1)
        current_raw = read_adc(1)
        current = ((current_raw * 3.3) / 1023 - 2.5) / 0.185

        print("Temp:", temperature, "C")
        print("Humidity:", humidity, "%")
        print("Pressure:", pressure, "hPa")
        print("Voltage:", round(voltage,2), "V")
        print("Current:", round(current,2), "A")
        print("Vibration:", vibration)

        # Threshold Conditions
        if (temperature > 50 or
            pressure > 1050 or
            vibration == 1 or
            voltage > 24 or
            current > 10):

            print("⚠ ALERT! Abnormal Condition")
            buzzer_alert()

        print("--------------------------")
        time.sleep(2)

except KeyboardInterrupt:
    print("System Stopped")

finally:
    GPIO.cleanup()
