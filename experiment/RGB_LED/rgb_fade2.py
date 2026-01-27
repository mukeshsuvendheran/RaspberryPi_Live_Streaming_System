import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
channel = [12, 13, 19]

for ch in channel: 
    GPIO.setup(ch, GPIO.OUT)

r_pwm = GPIO.PWM(12, 60)
g_pwm = GPIO.PWM(13, 60)
b_pwm = GPIO.PWM(19, 60)

# Start PWM at OFF state (100% for common anode)
r_pwm.start(100)
g_pwm.start(100)
b_pwm.start(100)

try:
    while True:
               # Fade OUT (decrease brightness)
        for dc in range(100, -1, -5):
            r_pwm.ChangeDutyCycle(dc)
            g_pwm.ChangeDutyCycle(dc)
            b_pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)


            for dc in range(0, 101, 5):
            r_pwm.ChangeDutyCycle(dc)
            g_pwm.ChangeDutyCycle(dc)
            b_pwm.ChangeDutyCycle(dc)
            time.sleep(0.1)

        
except KeyboardInterrupt:
    pass

r_pwm.stop()
g_pwm.stop()
b_pwm.stop()
GPIO.cleanup()