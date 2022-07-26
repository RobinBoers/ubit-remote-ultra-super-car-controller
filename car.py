from microbit import *
import math
from neopixel import NeoPixel
from time import sleep
import machine
import utime
from music import play,stop,BA_DING
import radio
import time

########################### Libraries ########################### 

# A module to simplify the driving o the motors on Kitronik :MOVE Motor buggy with micro:bit
CHIP_ADDR = 0x62 # CHIP_ADDR is the standard chip address for the PCA9632, datasheet refers to LED control but chip is used for PWM to motor driver
MODE_1_REG_ADDR = 0x00
MODE_2_REG_ADDR = 0x01
MOTOR_OUT_ADDR = 0x08 # MOTOR output register address
MODE_1_REG_VALUE = 0x00 # Setup to normal mode and not to respond to sub address
MODE_2_REG_VALUE = 0x04  # Setup to make changes on ACK, outputs set to open-drain
MOTOR_OUT_VALUE = 0xAA  # Outputs set to be controled PWM registers
LEFT_MOTOR = 0x04
RIGHT_MOTOR = 0x02
LF = pin2
LB = pin8
RF = pin1
RB = pin0
class MOVEMotorSensors:

    def distanceCm(self):
        pin14.set_pull(pin14.NO_PULL)
        pin13.write_digital(0)
        utime.sleep_us(2)
        pin13.write_digital(1)
        utime.sleep_us(10)
        pin13.write_digital(0)             
        distance = machine.time_pulse_us(pin14,1,1160000)
        if distance>0:
            return round(distance/58)
        else:
            return round(distance)

    def distanceInch(self):
        return (self.distanceCm() * 0.3937)

    def lineFollowCal(self):
        self.rightLineSensor = pin1.read_analog()
        self.leftLineSensor = pin2.read_analog()
        #calculate the middle value between the two sensor readings
        offset = abs(self.rightLineSensor-self.leftLineSensor)/2
        #apply the offset to each reading so that it neutralises any difference
        if self.leftLineSensor > self.rightLineSensor:
            self.leftLfOffset = -offset
            self.rightLfOffset = offset
        else:
            self.leftLfOffset = offset
            self.rightLfOffset = -offset
  
    def readLineFollow(self, sensor):
        if sensor == "left":
            return pin2.read_analog() + self.leftLfOffset
        elif sensor == "right":
            return pin1.read_analog() + self.rightLfOffset

class MOVEMotor:

    # An initialisation function to setup the PCA chip correctly
    def __init__(self):
    
        buffer = bytearray(2)
        buffer[0] = MODE_1_REG_ADDR
        buffer[1] = MODE_1_REG_VALUE
        i2c.write(CHIP_ADDR,buffer,False)
        buffer[0] = MODE_2_REG_ADDR
        buffer[1] = MODE_2_REG_VALUE
        i2c.write(CHIP_ADDR,buffer,False)
        buffer[0] = MOTOR_OUT_ADDR
        buffer[1] = MOTOR_OUT_VALUE
        i2c.write(CHIP_ADDR,buffer,False)

    # A couple of 'raw' speed functions for the motors.
    # These functions expect speed -255 -> +255
    def LeftMotor(self,speed):
        motorBuffer=bytearray(2)
        gndPinBuffer=bytearray(2)
        if(math.fabs(speed)>255):
            motorBuffer[1] = 255
        else:
            motorBuffer[1] = int(math.fabs(speed))
        gndPinBuffer[1] = 0x00
        if(speed >0):
            #going forwards
            motorBuffer[0] = LEFT_MOTOR
            gndPinBuffer[0] = LEFT_MOTOR +1
        else: #going backwards, or stopping
            motorBuffer[0] = LEFT_MOTOR +1
            gndPinBuffer[0] = LEFT_MOTOR
        i2c.write(CHIP_ADDR,motorBuffer,False)
        i2c.write(CHIP_ADDR,gndPinBuffer,False)

    # speed -255 -> +255
    def RightMotor(self,speed):
        motorBuffer=bytearray(2)
        gndPinBuffer=bytearray(2)

        if(math.fabs(speed)>255):
            motorBuffer[1] = 255
        else:
            motorBuffer[1] = int(math.fabs(speed))
        gndPinBuffer[1] = 0x00

        if(speed >0):
            #going forwards
            motorBuffer[0] = RIGHT_MOTOR +1
            gndPinBuffer[0] = RIGHT_MOTOR
        else: #going backwards
            motorBuffer[0] = RIGHT_MOTOR
            gndPinBuffer[0] = RIGHT_MOTOR +1

        i2c.write(CHIP_ADDR,motorBuffer,False)
        i2c.write(CHIP_ADDR,gndPinBuffer,False)

    # A function that stops both motors, rather than having to call Left and Right with zero speed.
    def StopMotors(self):
        stopBuffer=bytearray(2)
        stopBuffer[0] = LEFT_MOTOR
        stopBuffer[1] = 0x00
        i2c.write(CHIP_ADDR,stopBuffer,False)
        stopBuffer[0] = LEFT_MOTOR +1
        i2c.write(CHIP_ADDR,stopBuffer,False)
        stopBuffer[0] = RIGHT_MOTOR
        i2c.write(CHIP_ADDR,stopBuffer,False)
        stopBuffer[0] = RIGHT_MOTOR +1
        i2c.write(CHIP_ADDR,stopBuffer,False)
    
######################### Actually code ######################### 

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
