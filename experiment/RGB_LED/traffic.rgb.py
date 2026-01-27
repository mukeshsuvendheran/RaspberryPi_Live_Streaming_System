import RPi.GPIO as GPIO     
import time

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

class traffic():

    def all_off():
     r_pwm.ChangeDutyCycle(100)
     g_pwm.ChangeDutyCycle(100)
     b_pwm.ChangeDutyCycle(100)

    def on_red(pwm):   
        print("waiting 5 seconds in red🔴")
        traffic.all_off()
        pwm.ChangeDutyCycle(0)
        time.sleep(5)
     
    def on_yellow(pwm):   
        print("get ready 2 seconds in yellow🟡")
        pwm.ChangeDutyCycle(0)
        time.sleep(2)   
      

    def on_green(pwm):   
        print("Go and safe ride🟢")
        traffic.all_off()
        pwm.ChangeDutyCycle(0)
        time.sleep(5)
        print("----------x----------")
   

try:
    while True:
        traffic.on_red(r_pwm)   # Red
        traffic.on_yellow(g_pwm)   # Yellow
        traffic.on_green(g_pwm)   # Green
except KeyboardInterrupt:
    pass
r_pwm.stop()
g_pwm.stop()
b_pwm.stop()
GPIO.cleanup()
