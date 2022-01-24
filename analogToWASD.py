import pyautogui
from pyautogui import keyDown, keyUp, press
import inputs
import threading

pyautogui.PAUSE = 0

analogEnabled = False
epsilon = 0.01
intervalLength = 0.05
downTime = 0.01

axisList = []
class Axis:
    def __init__(self, low, high, eventCode, axisMax):
        self.low = low
        self.high = high
        self.state = 0
        self.eventCode = eventCode
        self.axisMax = axisMax

        axisList.append(self)

        threading.Thread(target=axisThread, args = (self,)).start()
    
    def key(self, invert = False):
        return self.low if (self.state < 0) != invert else self.high

    def onEvent(self, event):
        if event.code == self.eventCode:
            self.state = event.state

def axisThread(axis):
    while True:
        if analogEnabled:
            percent = abs(axis.state / axis.axisMax)
            print(percent)
            interval = (1 - percent) * intervalLength + downTime
            if percent > epsilon:
                press(axis.key(), interval = interval, _pause = False)

xAxis = Axis("num4", "num6", "ABS_RX", 32768)
yAxis = Axis("num8", "num5", "ABS_RY", 32768)
zAxis = Axis("s", "w", "ABS_Y", 32768)

buttonMap = {
    "BTN_TR": "e",
    "BTN_TL": "w",
    "BTN_SELECT": "space",
    "BTN_NORTH": "1",
    "BTN_SOUTH": "2"
}

while True:
    events = inputs.get_gamepad()
    for event in events:
        for axis in axisList:
            axis.onEvent(event)

        # code = event.code
        # if code.startswith("ABS"):
        #     print(event.code + ": " + str(event.state))

        if event.code == "BTN_START" and event.state == 1:
            analogEnabled = not analogEnabled
            print("Analog enabled =", analogEnabled)

        for button, key in buttonMap.items():
            if event.code == button:
                if event.state == 0:
                    keyUp(key)
                else:
                    keyDown(key)