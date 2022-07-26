# Module for simplifying communications with the Waveshare joystick for the micro:bit.
JoyStick_P = pin8
JoyStick_X = pin1
JoyStick_Y = pin2
KEY_A = pin5
KEY_B = pin11
KEY_C = pin15
KEY_D = pin14
KEY_E = pin13
KEY_F = pin12
DIR = {
    'NONE': 0,
    'U': 1,
    'D': 2,
    'L': 3,
    'R': 4,
    'U_L': 5,
    'U_R': 6,
    'D_L': 7,
    'D_R': 8
}
KEY = {
    'NONE': 0,
    'P': 1,
    'A': 2,
    'B': 3,
    'C': 4,
    'D': 5,
    'E': 6,
    'F': 7
}
SCALE = {
    'C': 262,
    'bD': 277,
    'D': 294,
    'bE': 311,
    'E': 330,
    'F': 349,
    'bG': 370,
    'G': 392,
    'bA': 415,
    'A': 440,
    'bB': 466,
    'B': 494,
    'C1': 523
}

class JOYSTICK():
    def __init__(self):
        self.Read_X = JoyStick_X.read_analog()
        self.Read_Y = JoyStick_Y.read_analog()

    def Listen_Dir(self, Dir):
        Get_Rocker = DIR['NONE']
        New_X = JoyStick_X.read_analog()
        New_Y = JoyStick_Y.read_analog()

        Dx = abs(self.Read_X - New_X)
        Dy = abs(self.Read_Y - New_Y)

        Right = New_X - self.Read_X
        Left = self.Read_X - New_X
        Up = New_Y - self.Read_Y
        Down = self.Read_Y - New_Y

        # max = 1023
        Precision = 150

        if Right > Precision and Dy < Precision:
            Get_Rocker = DIR['R']
        elif Left > Precision and Dy < Precision:
            Get_Rocker = DIR['L']
        elif Up > Precision and Dx < Precision:
            Get_Rocker = DIR['U']
        elif Down > Precision and Dx < Precision:
            Get_Rocker = DIR['D']
        elif Right > Precision and Up > Precision:
            Get_Rocker = DIR['U_R']
        elif Right > Precision and Down > Precision:
            Get_Rocker = DIR['D_R']
        elif Left > Precision and Up > Precision:
            Get_Rocker = DIR['U_L']
        elif Left > Precision and Down > Precision:
            Get_Rocker = DIR['D_L']
        else:
            Get_Rocker = DIR['NONE']

        if Dir == Get_Rocker:
            return True
        else:
            return False

    def Listen_Key(self, Key):
        read_key = KEY['NONE']
        if button_a.is_pressed():
            read_key = KEY['A']
        elif button_b.is_pressed():
            read_key = KEY['B']
        elif KEY_C.read_digital() == 0:
            read_key = KEY['C']
        elif KEY_D.read_digital() == 0:
            read_key = KEY['D']
        elif KEY_E.read_digital() == 0:
            read_key = KEY['E']
        elif KEY_F.read_digital() == 0:
            read_key = KEY['F']
        elif JoyStick_P.read_digital() == 0:
            read_key = KEY['P']
        else:
            read_key = KEY['NONE']

        if Key == read_key:
            return True
        else:
            return False

    def PlayScale(self, freq):
        millisec = 500
        music.pitch(freq, millisec)

    def Playmusic(self, tune):
        music.play(tune)

    def Test(self):
        while self.Listen_Dir(DIR['U']):
            display.show(Image.ARROW_N)
        while self.Listen_Dir(DIR['D']):
            display.show(Image.ARROW_S)
        while self.Listen_Dir(DIR['L']):
            display.show(Image.ARROW_W)
        while self.Listen_Dir(DIR['R']):
            display.show(Image.ARROW_E)
        while self.Listen_Dir(DIR['U_L']):
            display.show(Image.ARROW_NW)
        while self.Listen_Dir(DIR['U_R']):
            display.show(Image.ARROW_NE)
        while self.Listen_Dir(DIR['D_L']):
            display.show(Image.ARROW_SW)
        while self.Listen_Dir(DIR['D_R']):
            display.show(Image.ARROW_SE)
        while self.Listen_Key(KEY['A']):
            display.scroll("A")
        while self.Listen_Key(KEY['B']):
            display.scroll("B")
        while self.Listen_Key(KEY['C']):
            display.scroll("C")
        while self.Listen_Key(KEY['D']):
            display.scroll("D")
        while self.Listen_Key(KEY['E']):
            display.scroll("E")
        while self.Listen_Key(KEY['F']):
            display.scroll("F")
        while self.Listen_Key(KEY['P']):
            display.scroll("P")
        display.clear()
