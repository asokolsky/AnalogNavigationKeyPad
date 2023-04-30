import time
import board
from analogio import AnalogIn
#from typing import Float

from analog_navigation_keypad import AnalogNavigationKeypad, VirtualKey


class MyKeypad(AnalogNavigationKeypad):
    '''
    Example demonstrating how to use AnalogNavigationKeypad
    '''
    def __init__(self) -> None:
        # init superclass informing it to which pins the key pad is attached.
        super().__init__(board.G1, board.G2)
        return

    def onUserInActivity(self, ulNow:int) -> bool:
        print(f"onUserInActivity({ulNow})")
        return False

    def onKeyAutoRepeat(self, vk:VirtualKey) -> bool:
        print(f"onKeyAutoRepeat({vk})")
        return False

    def onKeyDown(self, vk:VirtualKey) -> bool:
        '''
        Return True is
        '''
        print(f"onKeyDown({vk})")
        return False

    def onLongKeyDown(self, vk:VirtualKey) -> bool:
        print(f"onLongKeyDown({vk})")
        return False

    def onKeyUp(self, vk:VirtualKey) -> bool:
        print(f"onKeyUp({vk})")
        return False


try:
    kp = MyKeypad()
    while True:
        #print(f"a1={a1.getRaw()} a2={a2.getRaw()}")
        now = round(time.time() * 1000)
        if kp.getAndDispatchKey(now):
            # something non-trivial happened
            # redraw the screen here
            pass
        time.sleep(kp.s_fDispatchInterval)

except RuntimeError as x:
    print(f"Caught: {x}")

except KeyboardInterrupt:
    print("Ciao")
