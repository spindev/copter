import time 
import pigpio 
import RPi.GPIO as GPIO
import os
import lib.XboxController as XboxController
import lib.Adafruit_BMP085 as barometer
import thread

MIN = 1000
MAX = 2500

FRONT_SPEED = MIN
BACK_SPEED = MIN

STEP = 20
SLEEP_TIME = 0.5

esc1 = 6
esc2 = 13
esc3 = 19
esc4 = 26 

front_l = esc3
front_r = esc1

back_l = esc4
back_r = esc2

calibrated = False

def setSpeedForAll(value):
    setSpeedFront(value)
    setSpeedBack(value)

def setSpeedFront(value):
    global FRONT_SPEED

    if FRONT_SPEED + value >= MAX or FRONT_SPEED + value < MIN:
        return

    FRONT_SPEED = FRONT_SPEED + value
    
    pi.set_servo_pulsewidth(front_l, FRONT_SPEED)
    pi.set_servo_pulsewidth(front_r, FRONT_SPEED)
    print("front speed: ") + str(FRONT_SPEED)

def setSpeedBack(value):
    global BACK_SPEED

    if BACK_SPEED + value >= MAX or BACK_SPEED + value < MIN:
        return

    BACK_SPEED = BACK_SPEED + value
    
    pi.set_servo_pulsewidth(back_l, BACK_SPEED)
    pi.set_servo_pulsewidth(back_r, BACK_SPEED)
    print("back speed: ") + str(BACK_SPEED)

def calibrate():
    global calibrated
    if calibrated == True:
        return

    print("calibrate...")
    calibrated = True
    pi.set_servo_pulsewidth(front_l, MAX)
    pi.set_servo_pulsewidth(front_r, MAX)
    pi.set_servo_pulsewidth(back_l, MAX)
    pi.set_servo_pulsewidth(back_r, MAX)
    time.sleep(2)
    pi.set_servo_pulsewidth(front_l, MIN)
    pi.set_servo_pulsewidth(front_r, MIN)
    pi.set_servo_pulsewidth(back_l, MIN)
    pi.set_servo_pulsewidth(back_r, MIN)
    time.sleep(2)
    print("lets fly...")

    return

def shutdown():
    print("shutdown...")
    restart()
    pi.stop()
    xboxCont.stop()
    os._exit(0)

def restart():
    pi.set_servo_pulsewidth(front_l, 0)
    pi.set_servo_pulsewidth(front_r, 0)
    pi.set_servo_pulsewidth(back_l, 0)
    pi.set_servo_pulsewidth(back_r, 0)

def setAlltoMin():
    global BACK_SPEED
    global FRONT_SPEED

    BACK_SPEED = MIN
    FRONT_SPEED = MIN

    pi.set_servo_pulsewidth(front_l, MIN)
    pi.set_servo_pulsewidth(front_r, MIN)
    pi.set_servo_pulsewidth(back_l, MIN)
    pi.set_servo_pulsewidth(back_r, MIN)

def startCallBack(value):
    if value == 0:
        return

    calibrate()

def backCallBack(value):
    if value == 0:
        return

    setAlltoMin()

def dpadCallBack(value):
    global SPEED

    setSpeedForAll(STEP * value[1])

def xboxCallBack(value):
    shutdown()
    
    return

def fligthControl(value):
    try:
        while True:
          #  time.sleep(SLEEP_TIME)
            print("pressure: ") + str(bmp.readAltitude())

    except KeyboardInterrupt:
	    print("stopping fligthcontrol...")

def rthumbCallBack(value):
    if value > 1:
       setSpeedFront(STEP)

    if value == -1:
       setSpeedFront(-1 * STEP)

def lthumbCallBack(value):
    if value > 1:
       setSpeedBack(STEP)

    if value == -1:
       setSpeedBack(-1 * STEP)
# Main

GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()
#bmp = barometer.BMP085(0x77, 3)

xboxCont = XboxController.XboxController(
    controllerCallBack = None,
    joystickNo = 0,
    deadzone = 0.1,
    scale = 1,
    invertYAxis = True)

xboxCont.setupControlCallback(xboxCont.XboxControls.START, startCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.BACK, backCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.DPAD, dpadCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.RTHUMBY, rthumbCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.LTHUMBY, lthumbCallBack)
xboxCont.setupControlCallback(xboxCont.XboxControls.XBOX, xboxCallBack)

restart()

#thread.start_new_thread(fligthControl, (True,))

print("init successfull...")

xboxCont.start()

try:
	while True:
		time.sleep(SLEEP_TIME)

except KeyboardInterrupt:
	print("interrupt...")

finally:
    shutdown()