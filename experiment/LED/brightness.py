import RPi.GPIO as GPIO

channel = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, 60)
p.start(0)

try:
    while True:
        d = input("set a BRIGHTNESS 1 to 100 or (q to quit): ")
        if d == "q":
            break

        try:
            p.ChangeDutyCycle(int(d))
        except ValueError:
            print("Please enter numbers only")

except KeyboardInterrupt:
    print("received ctrl + c -> Quitting")

finally:
    p.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
