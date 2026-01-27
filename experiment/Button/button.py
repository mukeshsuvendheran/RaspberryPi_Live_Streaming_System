import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  
BUTTON_PIN = 18
while True:
       if (GPIO.input(BUTTON_PIN) == GPIO.HIGH):
           print("Button Pressed")
           time.sleep(0.5)  