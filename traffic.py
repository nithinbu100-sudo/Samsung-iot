

import RPi.GPIO as GPIO
import time

# GPIO Pin Numbers
RED = 17
YELLOW = 27
GREEN = 22

GPIO.setmode(GPIO.BCM)

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

try:
    while True:
        # Green ON (Go)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(YELLOW, GPIO.LOW)
        GPIO.output(RED, GPIO.LOW)
        print("Green Light - GO")
        time.sleep(5)

        # Yellow ON (Wait)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(YELLOW, GPIO.HIGH)
        GPIO.output(RED, GPIO.LOW)
        print("Yellow Light - WAIT")
        time.sleep(2)

        # Red ON (Stop)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(YELLOW, GPIO.LOW)
        GPIO.output(RED, GPIO.HIGH)
        print("Red Light - STOP")
        time.sleep(5)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()