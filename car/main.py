from microbit import *
import math
from neopixel import NeoPixel
from time import sleep
import machine
import utime
from music import play,stop,BA_DING
import radio
import time

from move_motor import *
from map_num import *

amountOfLights = 4
lightControlPin = pin8

buggy = MOVEMotor()
sensor = MOVEMotorSensors()
buggyLights = NeoPixel(lightControlPin, amountOfLights)

# Colors
redLightColor = [200,0,0]
blueLightColor = [200,200,255]
greenLightColor = [0,150,0]

# Constants
# makes sure the buggy doesn't lose the line. 80 is slow and sometimes gets stuck, 65 is around the sweet spot, fast but reliable. 60 is slightly faster, and with everything below it can't make certain turns anymore
speedLimiter = 57  
turboModeModifier = 50 # extra speed on straight lines
motorOffset = -15   # compensates for the difference between the Left    
                    # and Right Motor

followingLine = True
angryMode = False

speedX = 0
speedY = 0

def init():
    global sensor
    
    radio.on()
    radio.config(queue=20, channel=30)
    sensor.lineFollowCal(sensor)

    main()

def main():
    global angryMode, followingLine, motorOffset
    while True:
        incoming = radio.receive()

        if followingLine == True:
            followLine(incoming)
        else:
            manuallyDriveCar(incoming)

        if incoming == "buggy_toggle_alarm":
            angryMode = not angryMode
            time.sleep(0.2)
        
        elif incoming == "buggy_toggle_line_follow":
            followingLine = not followingLine
            time.sleep(0.2)

        elif incoming == "buggy_increase_offset":
            motorOffset += 1

        elif incoming == "buggy_decrease_offset":
            motorOffset -= 1
        
        setLights()
        buggyLights.show()

def followLine(incoming):
    global buggy, sensor, speedLimiter, motorOffset, turboModeModifier\
        
    leftSensor = sensor.readLineFollow(sensor, "left")
    rightSensor = sensor.readLineFollow(sensor, "right")

    # print("left sensor " + str(leftSensor) + " right sensor " + str(rightSensor))

    speedL = leftSensor - speedLimiter
    speedR = rightSensor + motorOffset - speedLimiter
    
    if incoming == "buggy_nudge":
        speedL += 10
        speedR += 10
        
    # if the car is in line following mode and on a straight line,
    # drastically increase the speed. Also called "TURBO MODE!!".
    if abs(speedL - speedR) < 10:
        speedL += turboModeModifier
        speedR += turboModeModifier

    buggy.LeftMotor(speedL)
    buggy.RightMotor(speedR)

def manuallyDriveCar(incoming):
    global speedX, speedY
    incoming = str(incoming)

    if incoming[0:7] == "buggy_X":
        speedX = int(incoming[8:len(incoming)])
    elif incoming[0:7] == "buggy_Y":
        speedY = int(incoming[8:len(incoming)])

    drive(speedX, speedY)

def setLights():
    if angryMode == True:
        setAngryLights()
    else:
        if followingLine == True:
            display.show(Image.ASLEEP)
        else:
            setDefaultLights()

def setDefaultLights():
    buggyLights[0] = blueLightColor
    buggyLights[1] = blueLightColor
    buggyLights[2] = redLightColor
    buggyLights[3] = redLightColor
    display.show(Image.HAPPY)

def setAngryLights():
    buggyLights[0] = redLightColor 
    buggyLights[1] = redLightColor 
    buggyLights[2] = redLightColor 
    buggyLights[3] = redLightColor 
    display.show(Image.ANGRY)

def drive(X, Y):
    global motorOffset, followingLine
    baseSpeed = getBaseSpeed()
    
    X = int(X*1)
    Y = int(Y*1)
    
    factorY = mapNum(Y, 0, 1023, -1, 1)
    speedForward = baseSpeed * factorY
    
    reductionR = 0
    reductionL = 0

    if X > 512:
        reductionR = mapNum(X, 512, 1023, 0, 1)
    elif X < 512:
        reductionL = 1 - mapNum(X, 0, 512, 0, 1)

    speedL = speedForward
    speedR = speedForward + motorOffset

    speedL = speedL - speedL * reductionL
    speedR = speedR - speedR * reductionR

    offset = 100
    if Y > 512-offset and Y < 512+offset:        
        factorX = mapNum(X, 0, 1023, -1, 1)
        speedL = baseSpeed * factorX
        speedR = baseSpeed * -factorX + motorOffset
    
    buggy.LeftMotor(speedL)
    buggy.RightMotor(speedR)

def getBaseSpeed():
    global angryMode
    if angryMode == True:
        return 255
    else:
        return 155

init()