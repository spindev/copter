import time 
import pigpio 
import RPi.GPIO as GPIO
import os
import lib.XboxController as XboxController

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
    print("speed: ") + str(value)

def calibrate():
    print("Calibrate...")
    setSpeed(MAX)
    time.sleep(2)
    setSpeed(MIN)
    time.sleep(2)
    print("lets fly...")

    return

def finish():
    setSpeed(0)
    pi.stop()
    xboxCont.stop()
    os._exit(0)

def startCallBack(value):
    if value == 0:
        return

    calibrate()

def dpadCallBack(value):
    global SPEED

    if(value[0] == 1 and SPEED < MAX):
        SPEED = SPEED + STEP
        setSpeed(SPEED)

    if(value[0] == -1 and SPEED > MIN):
        SPEED = SPEED - STEP
        setSpeed(SPEED)

# Main

GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()

xboxCont = XboxController.XboxController(
    controllerCallBack = None,
    joystickNo = 0,
    deadzone = 0.1,
    scale = 1,
    invertYAxis = True)

xboxCont.setupControlCallback(xboxCont.XboxControls.START, startCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.BACK, finish)
xboxCont.setupControlCallback(xboxCont.XboxControls.DPAD, dpadCallBack)

xboxCont.start()

print("init successfull...")

try:
	while True:
		time.sleep(SLEEP_TIME)
	
except KeyboardInterrupt:
	print("end...")

finally:
    finish()