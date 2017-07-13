import time 
import pigpio 
import RPi.GPIO as GPIO
import os
import lib.xbox as xbox
import thread
import lib.gyroa as gyro

MIN = 1000
MAX = 2500

SPEED = MIN

STEP = 100
CONTROL_STEP = 5

SLEEP_TIME = 0.5

front_l = 19
front_r = 6

back_l = 26
back_r = 13

speeds = {front_l : MIN, front_r : MIN, back_l : MIN, back_r : MIN}

# front_l up -> x < 0
# front_r up -> y > 0

calibrated = False
fligthtModeEnabled = False

def setAbsoluteSpeed(value):
    pi.set_servo_pulsewidth(front_l, value)
    pi.set_servo_pulsewidth(front_r, value)
    pi.set_servo_pulsewidth(back_l, value)
    pi.set_servo_pulsewidth(back_r, value)

def setSpeedForAll(value):
    global SPEED
    global speeds

    SPEED = SPEED + value

    if SPEED > MAX or SPEED < MIN:
        return

    speeds[front_l] = SPEED
    speeds[front_r] = SPEED
    speeds[back_l] = SPEED
    speeds[back_r] = SPEED

    print("current speed: " + str(SPEED))

    setAbsoluteSpeed(SPEED)

def setSpeed(esc, value):
    global speeds

    speeds[esc] = speeds[esc] + value

    if speeds[esc] > MAX or speeds[esc] < MIN or speeds[esc] > SPEED + STEP:
        return

    print(str(esc) + " speed: " + str(speeds[esc]))

    pi.set_servo_pulsewidth(esc, speeds[esc])

def calibrate():
    global calibrated

    if calibrated == True:
        return

    print("calibrate...")
    setAbsoluteSpeed(MAX)
    time.sleep(2)
    setAbsoluteSpeed(MIN)
    time.sleep(2)
    print("lets fly...")

    calibrated = True

    return

def shutdown():
    print("shutdown...")
    restart()
    pi.stop()
    joy.close()
    os._exit(0)

def restart():
    setAbsoluteSpeed(0)

def setAlltoMin():
    global SPEED
    global fligthtModeEnabled
    
    SPEED = MIN

    print("current speed: " + str(SPEED))

    setAbsoluteSpeed(SPEED)
        
    fligthtModeEnabled = False

def startCallBack(value):
    if value == 0:
        return

    calibrate()

def backCallBack(value):
    if value == 0:
        return

    setAlltoMin()

def dpadCallBack(value):
    global fligthtModeEnabled

    fligthtModeEnabled = True
    
    setSpeedForAll(value)

def xboxCallBack(value):
    shutdown()
    
    return

# Main

GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()

joy = xbox.Joystick()

restart()

print("init successfull...")

try:
	while True:
            time.sleep(0.08)

            if joy.Start():
                calibrate()
            
            if joy.Back():
                setAlltoMin()

            if joy.Guide():
                shutdown()

            if joy.dpadUp():
                dpadCallBack(STEP)

            if joy.dpadDown():
                dpadCallBack(-STEP)

            #print("test")
            if fligthtModeEnabled == False:
                continue

            if gyro.getXrotation() < 0:
                setSpeed(back_r, CONTROL_STEP)

            if gyro.getXrotation() > 0:
                setSpeed(front_l, CONTROL_STEP)

            if gyro.getYrotation() > 0:
                setSpeed(back_l, CONTROL_STEP)

            if gyro.getYrotation() < 0:
                setSpeed(front_r, CONTROL_STEP)

except KeyboardInterrupt:
	print("interrupt...")

finally:
    shutdown()