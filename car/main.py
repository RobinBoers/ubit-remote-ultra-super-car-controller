from microbit import *
import math
from neopixel import NeoPixel
from time import sleep
import machine
import utime
from music import play,stop,BA_DING
import radio
import time

import move_motor

buggy = MOVEMotor()
buggyLights = NeoPixel(pin8, 4)

sensor = MOVEMotorSensors
sensor.lineFollowCal(sensor)

# Colors
redLightColor = [200,0,0]
blueLightColor = [200,200,255]
greenLightColor = [0,150,0]

# Constants
speedLimiter = 57  
# 80 is slow and sometimes gets stuck, 65 is around the sweet spot, fast but reliable. 60 is slightly faster, and with everything below it can't make certain turns anymore

followingLine = False
angryMode = False

def init():
    radio.on()
    radio.config(queue=20)
    main()

def main():
    while True:
        incoming = radio.receive()
        imcoming = str(incoming)

        setSpeedForMode(angryMode)

        if followingLine == True:
            followLine()
        else:
            manuallyDriveCar()

        if incoming == "buggy_toggle_alarm":
            angryMode = not angryMode
            time.sleep(0.2)
        
        elif incoming == "buggy_toggle_line_follow":
            followingLine = not followingLine
            time.sleep(0.2)
        
        setLights()

        buggyLights.show()

def setSpeedForMode(angryModeOn):
    if angryModeOn == True:
        baseSpeed = 255
    else:
        baseSpeed = 155

    maxSpeed = baseSpeed
    turnSpeed = maxSpeed - 50

def followLine():
    leftSensor = sensor.readLineFollow(sensor, "left")
    rightSensor = sensor.readLineFollow(sensor, "right")
    
    buggy.LeftMotor(leftSensor + leftMotorOffset - speedLimiter)
    buggy.RightMotor(rightSensor + rightMotorOffset - speedLimiter)

def manuallyDriveCar():
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

# Motor control

rightMotorOffset = 2
leftMotorOffset = 0
speedX = 0
speedY = 0

def drive(X, Y):
    X = int(X*1)
    Y = int(Y*1)

    if Y > 482 and Y < 542:
        factorX = mapNum(X, 0, 1023, -1, 1)
        buggy.LeftMotor(baseSpeed * factorX)
        buggy.RightMotor(baseSpeed * -factorX)
        return
    
    factorY = mapNum(Y, 0, 1023, -1, 1)
    speedForward = baseSpeed * factorY
    speedL = speedForward
    speedR = speedForward
    reductionR = 0
    reductionL = 0
    
    if X > 512:
        reductionR = mapNum(X, 512, 1023, 0, 1)
    elif X < 512:
        reductionL = 1- mapNum(X, 0, 512, 0, 1)
    
    buggy.LeftMotor(speedL - speedL * reductionL)
    buggy.RightMotor(speedR - speedR * reductionR)

# Utils

def mapNum(input, inMin, inMax, outMin, outMax):
    diffFromZero = 0 - inMin
    input += diffFromZero
    inMax += diffFromZero
    factor = input/inMax
    outRange = outMax-outMin
    diffFromZero = 0 - outMin
    output = outRange*factor
    output -= diffFromZero
    return output