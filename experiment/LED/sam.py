import RPi.GPIO as GPIO

channel = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, 60)
p.start(0)

try:
    while True:
        d = input("set a dutycycle (q to quit): ")
        if d == "q":
            break

        f = input("set a frequency (q to quit): ")
        if f == "q":
            break

        try:
            p.ChangeDutyCycle(int(d))
            p.ChangeFrequency(int(f))
        except ValueError:
            print("Please enter numbers only")

except KeyboardInterrupt:
    print("received ctrl + c -> Quitting")

finally:
    p.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
