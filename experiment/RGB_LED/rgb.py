import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BCM)
channel =[12,13,19]
for ch in channel:
    GPIO.setup(ch, GPIO.OUT)    
try:
    while True:
        num = input("Enter a number between 0-7: ")
        num = int(num)
        if num < 0 or num > 7:
            print("Invalid input, please enter a number between 0-7")
            continue

        for i, ch in enumerate(channel):
            print(i, ch)
            if (num >> i) & 1:                          # &1 (001)
                GPIO.output(ch, GPIO.HIGH)
            else:
                GPIO.output(ch, GPIO.LOW)   

# for ex : num=5(101)       
#j (bit)	GPIO	Calculation	Result
#0	12	(5 >> 0) & 1 → 1	HIGH
#1	13	(5 >> 1) & 1 → 0	LOW
#2	19	(5 >> 2) & 1 → 1	HIGH

#its comparing each bit of num with 1 of (101) 
#Right shift: 101 >> 0 = 101
#101
#001
#001  → 1 high (hereafter shift another right shift 1 and 2) 

except KeyboardInterrupt:
    pass    
GPIO.cleanup()  
print("GPIO cleaned up")