import RPi.GPIO as GPIO
channel = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, 0.5)  # frequency=60Hz
p.start(0)
try:        
    while True:

        
        try:
            d = (input("set a dutycycle:"))
            f = (input("set a frequency:"))

            if (d=='q' or f=='q'):
                break

            p.ChangeDutyCycle(int(d))
            p.ChangeFrequency(int(f))

        except ValueError as e:
          pass
except KeyboardInterrupt as e:
    print("received cnrt + c -> Quitting")
p.stop()
GPIO.cleanup()
print("GPIO cleaned up")
