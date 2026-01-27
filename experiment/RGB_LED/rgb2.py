import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
channel = [12, 13, 19]

for ch in channel: 
    GPIO.setup(ch, GPIO.OUT)

try:
    while True:
        num = int(input("Enter a number between 0-7: "))

        if num < 0 or num > 7:
            print("Invalid input")
            continue

        rgb = format(num, '03b')
        print("RGB binary:", rgb)

        for i, ch in enumerate(channel):
            print(f"Bit {i}, GPIO {ch}, Value {rgb[i]}")
            if (num >> i) & 1:
                GPIO.output(ch, GPIO.HIGH)
            else:
                GPIO.output(ch, GPIO.LOW)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
print("GPIO cleaned up")
