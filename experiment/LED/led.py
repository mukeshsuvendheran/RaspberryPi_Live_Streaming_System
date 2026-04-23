import RPi.GPIO  as GPIO
channel = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, 0.5)  # frequency=60Hz
p.start(1)

input("enter a key to quit")
p.stop()
GPIO.cleanup()