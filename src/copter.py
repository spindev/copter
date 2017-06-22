import time 
import lib.xbox as xbox 
import pigpio 
import RPi.GPIO as GPIO

MIN = 1000
MAX = 2500

SPEED = 1000

STEP = 100
SLEEP_TIME = 0.5

esc1 = 6
esc2 = 13
esc3 = 19
esc4 = 26 

def setSpeed(value):
	pi.set_servo_pulsewidth(esc1, value)
    	pi.set_servo_pulsewidth(esc2, value)
	pi.set_servo_pulsewidth(esc3, value)
	pi.set_servo_pulsewidth(esc4, value)

def calibrate():
    setSpeed(MAX)
    time.sleep(2)
    setSpeed(MIN)
    time.sleep(2)

    return

# Main

GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()
joy = xbox.Joystick()

print("Calibrate...")

calibrate()

print("Lets FLY...") 

try:
	while not joy.Back():
		if joy.dpadUp() and  SPEED < MAX:
			SPEED = SPEED + STEP
		
		if joy.dpadDown() and SPEED > MIN:
			SPEED = SPEED - STEP
	
		setSpeed(SPEED)
		print "Speed: " + str(SPEED)
		time.sleep(SLEEP_TIME)	
	
except KeyboardInterrupt:
	print "End..." 

finally:
    	setSpeed(0)
    	pi.stop()
	joy.close()
	
