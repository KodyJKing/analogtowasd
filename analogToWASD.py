import pyautogui
from pyautogui import keyDown, keyUp, press
import inputs
import threading

pyautogui.PAUSE = 0

axisMax = 32768
analogEnabled = False
epsilon = 0.1
intervalLength = 0.1
downTime = 0.01

axisList = []
class Axis:
    def __init__(self, low, high, eventCode):
        self.low = low
        self.high = high
        self.state = 0
        self.eventCode = eventCode

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
            percent = abs(axis.state / axisMax)
            interval = (1 - percent) * intervalLength + downTime
            if percent > epsilon:
                press(axis.key(), interval = interval, _pause = False)

xAxis = Axis("num4", "num6", "ABS_RX")
yAxis = Axis("num5", "num8", "ABS_RY")
# zAxis = Axis("0", "e", "ABS_Y")666666

buttonMap = {
    "BTN_TL": "e",
    "BTN_TR": "q",
    "BTN_SELECT": "space",
    "BTN_NORTH": "1"
}

while True:
    events = inputs.get_gamepad()
    for event in events:
        for axis in axisList:
            axis.onEvent(event)

        # print(event.code)

        if event.code == "BTN_START" and event.state == 1:
            analogEnabled = not analogEnabled
            print("Analog enabled =", analogEnabled)

        for button, key in buttonMap.items():
            if event.code == button:
                if event.state == 0:
                    keyUp(key)
                else:
                    keyDown(key)