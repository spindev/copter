import time 
import pigpio 
import RPi.GPIO as GPIO
import os
import lib.XboxController as XboxController

MIN = 1000
MAX = 2000

SPEED = MIN

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
    print("shutdown...")
    setSpeed(0)
    pi.stop()
    xboxCont.stop()
    os._exit(0)

def startCallBack(value):
    if value == 0:
        return

    calibrate()

def backCallBack(value):
    if value == 0:
        return

    finish()

def dpadCallBack(value):
    global SPEED

    if(value[1] == 1 and SPEED < MAX):
        SPEED = SPEED + STEP
        setSpeed(SPEED)

    if(value[1] == -1 and SPEED > MIN):
        SPEED = SPEED - STEP
        setSpeed(SPEED)
      
def lthumbCallBack(value):
    global SPEED

    SPEED = (1 + value) * 1250;

    if SPEED < MAX and SPEED > MIN:
        setSpeed(SPEED)

def xboxCallBack(value):
    global SPEED

    SPEED = MIN

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
xboxCont.setupControlCallback(xboxCont.XboxControls.BACK, backCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.DPAD, dpadCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBY, lthumbCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.XBOX, xboxCallBack)

xboxCont.start()

print("init successfull...")

try:
	while True:
		time.sleep(SLEEP_TIME)
	
except KeyboardInterrupt:
	print("end...")

finally:
    finish()