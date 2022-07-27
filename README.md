This is a super amazing fantastic ultra cool remote-controlled car that has been built using the [Kitronik :MOVE motor](https://opencircuit.nl/Product/Kitronik-MOVE-Motor-voor-de-BBC-micro-bit) and [Waveshare joystick](https://www.waveshare.com/joystick-for-micro-bit.htm) for the micro:bit. It has an optional line-following mode and is definitely going to beat Bas' car!

## Usage

To get the car up and running:

1. Open the micropython editor on <https://python.microbit.org> and copy the contents from [`car/main.py`](car/main.py) to the main editor area.

2. Download the [`map_num.py`](car/map_num.py) file and [upload it via Load/Save](https://support.microbit.org/support/solutions/articles/19000098018-files-and-modules-in-the-python-editor) in the editor.

3. Do the same for [`move_motor.py`](car/move_motor.py)

4. Plug in the micro:bit and [flash it using WebUSB](https://support.microbit.org/support/solutions/articles/19000105428-webusb-troubleshooting).

Make sure to turn on the car when you power the micro:bit. The program will only start if the car is on. You can always restart the micro:bit with the reset button on the back if things go wrong.

To get the controller work:

1. Open the micropython editor again and paste the contents of [`controller/main.py`](controller/main.py) in the main editor area.

2. Upload the [`waveshare_controller.py`](car/waveshare_controller.py), this is done the same as for the car.

3. Flash the micro:bit.

4. Profit.
