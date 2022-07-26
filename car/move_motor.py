# A module to simplify the driving of the motors on Kitronik :MOVE Motor buggy with micro:bit

# Source: 
# - https://github.com/KitronikLtd/micropython-microbit-kitronik-MOVE-motor-sensors
# - https://github.com/KitronikLtd/micropython-microbit-kitronik-MOVE-motor
# License: MIT License

from microbit import *
import math

CHIP_ADDR = 0x62 # CHIP_ADDR is the standard chip address for the PCA9632, datasheet refers to LED control but chip is used for PWM to motor driver
MODE_1_REG_ADDR = 0x00
MODE_2_REG_ADDR = 0x01
MOTOR_OUT_ADDR = 0x08 # MOTOR output register address
MODE_1_REG_VALUE = 0x00 # Setup to normal mode and not to respond to sub address
MODE_2_REG_VALUE = 0x04  # Setup to make changes on ACK, outputs set to open-drain
MOTOR_OUT_VALUE = 0xAA  # Outputs set to be controled PWM registers
LEFT_MOTOR = 0x04
RIGHT_MOTOR = 0x02

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

# MIT License

# Copyright (c) 2020 Kitronik Ltd 

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.