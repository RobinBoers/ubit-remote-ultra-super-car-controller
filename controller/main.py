from microbit import *
import music
import radio
import time

from waveshare_controller import *

JoyStick = JOYSTICK()
angryMode = False
    
def init():
    radio.on()
    radio.config(channel=30)
    display.show(Image.HAPPY)
    main()
    
def main():
    while True:   
        sendCoords()

        if JoyStick.Listen_Key(KEY['E']):
            toggleAngryMode()

        elif JoyStick.Listen_Key(KEY['F']):
            toggleLineFollow()

        elif JoyStick.Listen_Key(KEY['A']):
            decreaseMotorOffset()

        elif JoyStick.Listen_Key(KEY['B']):
            increaseMotorOffset()

        elif JoyStick.Listen_Key(KEY['C']):
            nudge()

        time.sleep(0.1)

def sendCoords():
    x_value = JoyStick_X.read_analog()
    y_value = JoyStick_Y.read_analog()
    
    radio.send("buggy_X_"+ str(x_value))
    radio.send("buggy_Y_"+ str(y_value))
    
def toggleAngryMode():
    global angryMode
    radio.send("buggy_toggle_alarm")
    angryMode = not angryMode

    if angryMode == True:
        display.show(Image.ANGRY)
    else:
        display.show(Image.HAPPY)

    time.sleep(0.1)

def toggleLineFollow():
    radio.send("buggy_toggle_line_follow")

def decreaseMotorOffset():
    radio.send("buggy_decrease_offset")

def increaseMotorOffset():
    radio.send("buggy_increase_offset")

def nudge():
    radio.send("buggy_nudge")

init()
