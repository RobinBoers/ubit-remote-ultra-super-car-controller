from microbit import *
import math
from neopixel import NeoPixel
from time import sleep
import machine
import utime
from music import play,stop,BA_DING
import radio
import time

# Radio
radio.on()
radio.config(queue=20)
        
# Motors
buggy = MOVEMotor()

# Colors
redLightColor = [200,0,0]
blueLightColor = [200,200,255]
greenLightColor = [0,150,0]

buggyLights = NeoPixel(pin8, 4)

# Sensors
sensor =  MOVEMotorSensors
sensor.lineFollowCal(sensor)

# Constants
speedLimiter = 57  #80
followingLine = False
angryMode = False

rightMotorOffset = 2
leftMotorOffset = 0
speedX = 0
speedY = 0

while True:
    incoming = radio.receive()
    
    if angryMode == True:
		baseSpeed = 255
    else:
	    baseSpeed = 155
    
    maxSpeed = baseSpeed
    turnSpeed = maxSpeed - 50
        
    if followingLine == True:
        leftSensor = sensor.readLineFollow(sensor, "left")
        rightSensor = sensor.readLineFollow(sensor, "right")
        
        buggy.LeftMotor(leftSensor + leftMotorOffset - speedLimiter)
        buggy.RightMotor(rightSensor + rightMotorOffset - speedLimiter)
        
    else: 
        incoming = str(incoming)
        
        if incoming[0:7] == "buggy_X":
            speedX = int(incoming[8:len(incoming)])
        elif incoming[0:7] == "buggy_Y":
            speedY = int(incoming[8:len(incoming)])
            
        drive(speedX, speedY)
        
    if incoming == "buggy_toggle_alarm":
        angryMode = not angryMode
        time.sleep(0.2)
        
    elif incoming == "buggy_toggle_line_follow":
        followingLine = not followingLine
        time.sleep(0.2)
    
    if angryMode == True:
        buggyLights[0] = redLightColor 
        buggyLights[1] = redLightColor 
        buggyLights[2] = redLightColor 
        buggyLights[3] = redLightColor 
        display.show(Image.ANGRY)
    else:
        if followingLine == True:
            display.show(Image.ASLEEP)
        else:
            buggyLights[0] = blueLightColor
            buggyLights[1] = blueLightColor
            buggyLights[2] = redLightColor
            buggyLights[3] = redLightColor
            display.show(Image.HAPPY)
            
    buggyLights.show()
    
def drive(X, Y):
    # Below is an adjustment to correct for motor speed discrepancy
    X = int(X*1)
    Y = int(Y*1)
    if Y>482 and Y<542:
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
