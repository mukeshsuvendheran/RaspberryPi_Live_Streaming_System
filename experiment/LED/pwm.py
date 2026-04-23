import RPi.GPIO  as GPIO
channel = 19
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)

p = GPIO.PWM(channel, 0.5)  # frequency=60Hz
p.start(1)
i = None
try:
while i != q :
    try:
        d = int(input("set a dutycycle:"))
        f = int(input("set a frequency:"))

        if(d ='q' or f ='q'):
            break;
    except ValueError as e:
        pass
except KeyboardInterrupt as e:
print("received cnrt + c -> Quitting") 

p.stop()
GPIO.cleanup()
print("i am exciting")