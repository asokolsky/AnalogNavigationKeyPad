#
# Python class to operate an analog navigation keypad
# https://oshwlab.com/asokolsky/Analog_Navigation_Keypad-a25307c2a2254b4eb4a9cd3543392b90
# https://oshwlab.com/asokolsky/Analog_Navigation_Keypad_copy-e961efefbccf49cd99776f7c87a63a96
#
# connected to USB->GPIO board e.g. MCP2221A Breakout
#

from analogio import AnalogIn
from enum import Enum
from typing import List, Set, Union

class VirtualKey( str, Enum ):
    '''
    Symbols for keys
    '''

    VK_NONE  = 'VK_NONE'
    VK_RIGHT = 'VK_RIGHT'
    VK_LEFT  = 'VK_LEFT'
    VK_UP    = 'VK_UP'
    VK_DOWN  = 'VK_DOWN'
    VK_SEL   = 'VK_SEL'
    VK_SOFTA = 'VK_SOFTA'
    VK_SOFTB = 'VK_SOFTB'

    @classmethod
    def is_valid( cls, st: Union[ str, 'VirtualKey' ] ) -> bool:
        return st in VirtualKey._value2member_map_

    def __repr__( s ) -> str:
        'To enable serialization as a string...'
        return repr( s.value )

VirtualKeys = Set[VirtualKey]

class AnalogNavigationKeypad:
    '''
    Base class - user will derive from this and overwrite the callback methods
    '''
    #
    # delay in ms before the long key is fired
    #
    s_iLongKeyDelay = 3000
    #
    # delay in ms before first auto-repeat fired
    #
    s_iAutoRepeatDelay = 500
    #
    # delay in ms before auto-repeats
    #
    s_iAutoRepeatInterval = 200
    #
    # inactivity timeout in milliseconds
    #
    s_iInactivityDelay = 10000
    #
    # delay in ms to debounce
    #
    s_iDebounceDelay = 50
    #
    # call getAndDispatchKey this often
    #
    s_fDispatchInterval = 0.020


    class KeypadChannel:
        '''
        Low level class important for implementation only
        '''

        def __init__(self, pin:AnalogIn, keys:List[VirtualKey]) -> None:
            # Analog pin from which we are reading
            self.m_pin = AnalogIn(pin)
            # when to fire long key
            self.m_iToFireLongKey = 0
            # when bouncing subsides
            self.m_iBounceSubsided = 0
            # when to fire key auto repeat
            self.m_iToFireAutoRepeat = 0

            # a set of scan codes to generate when one of keys is pressed
            self.m_keys = keys
            self.m_bOldKey = VirtualKey.VK_NONE
            return


        def getAndDispatchKey(
                self,
                ulNow:int,
                kp:"AnalogNavigationKeypad",
                uKeyOtherChannel:VirtualKey) -> bool:
            '''

            '''
            #print(f"getAndDispatchKey({ulNow})")

            # get out if we are bouncing!
            if(ulNow < self.m_iBounceSubsided):
                #print(f"getAndDispatchKey({ulNow}) => still bouncing")
                return False

            bRes = False
            vk = self.getKey()
            #print(f"{self}.getKey() => {vk}")
            if(vk == self.m_bOldKey):
                if(vk == VirtualKey.VK_NONE):
                    if(not kp.isUserLongInactive(ulNow)):
                        return False
                    bRes = kp.onUserInActivity(ulNow)
                    kp.onUserActivity(ulNow)
                    return bRes

                # fire long key logic here
                if((self.m_iToFireLongKey != 0)
                        and (ulNow >= self.m_iToFireLongKey)):
                    self.m_iToFireLongKey = 0
                    #print(f"onLongKeyDown vk={vk}")
                    return kp.onLongKeyDown(vk) or bRes

                # fire auto repeat logic here
                if((self.m_iToFireAutoRepeat != 0)
                        and (ulNow >= self.m_iToFireAutoRepeat)):
                    # arm auto-repeat
                    self.m_iToFireAutoRepeat = ulNow + kp.s_iAutoRepeatInterval
                    return kp.onKeyAutoRepeat(vk)

                return bRes

            # vk != m_cOldKey
            if(self.m_iBounceSubsided == 0):
                self.m_iBounceSubsided = ulNow + kp.s_iDebounceDelay
                return False

            if(self.m_bOldKey == VirtualKey.VK_NONE):
                # arm log-key
                self.m_iToFireLongKey = ulNow + kp.s_iLongKeyDelay
                # arm auto-repeat
                self.m_iToFireAutoRepeat = ulNow + kp.s_iAutoRepeatDelay
                self.m_iBounceSubsided = 0
                #print(f"calling onKeyDown vk={vk}, m_bOldKey={self.m_bOldKey}")
                bRes = kp.onKeyDown(vk)
                kp.onUserActivity(ulNow)

            elif(vk != VirtualKey.VK_NONE):
                # ignore transients!
                return False

            else:
                self.m_iToFireAutoRepeat = 0
                self.m_iToFireLongKey = 0
                self.m_iBounceSubsided = 0
                #print(f"calling onKeyUp vk={vk}, m_bOldKey={self.m_bOldKey}")
                bRes = kp.onKeyUp(self.m_bOldKey)
                kp.onUserActivity(ulNow)

            self.m_bOldKey = vk
            return bRes

        #def resetToFireAutoRepeat(self) -> None:
        #    '''reset when to fire auto repeat'''
        #    self.m_iToFireAutoRepeat = 0
        #    return

        def getKey(self) -> VirtualKey:
            '''
            read from the pin, return one of VK_xxx
            '''
            def getKey2(iReading: int) -> VirtualKey:
                '''
                get one of VK_xxx
                '''
                if(iReading > 48640):
                    #DEBUG_PRINTLN("Keypad::getKey2() => VK_NONE")
                    return VirtualKey.VK_NONE
                if(iReading < 16384):
                    #DEBUG_PRINTLN("Keypad::getKey2() => m_vk[0]")
                    return self.m_keys[0]
                #DEBUG_PRINTLN("Keypad::getKey2() => m_vk[1]")
                return self.m_keys[1]

            def getKey3(iReading: int) -> VirtualKey:
                '''
                get one of VK_xxx
                '''
                # 1st option for speed reasons since it is the most likely result
                if(iReading > 54528):
                    #print("KeypadChannel::getKey3() => VK_NONE")
                    return VirtualKey.VK_NONE
                if(iReading < 10880):
                    #print("KeypadChannel::getKey3, iReading=0x") DEBUG_PRINTHEX(iReading)DEBUG_PRINTLN(" => m_vk[0]")
                    return self.m_keys[0]
                if(iReading < 32704):
                    #DEBUG_PRINTLN(" => m_vk[1]")
                    return self.m_keys[1]
                #DEBUG_PRINTLN(" => m_vk[2]")
                return self.m_keys[2]

            def getKey4(iReading: int) -> VirtualKey:
                '''
                get one of VK_xxx
                '''
                # 1st option for speed reasons since it will be the most likely result
                #if(iReading > 60800):
                #    #DEBUG_PRINTLN(" => VK_NONE")
                #    return VirtualKey.VK_NONE
                if(iReading < 4864):
                    return self.m_keys[0]
                if(iReading < 22528): # (223+481)/2 = 352
                    return self.m_keys[1]
                if(iReading < 39552): # (481+755)/2 = 618
                    return self.m_keys[2]
                return self.m_keys[3]

            adc_key_in = self.m_pin.value # read the value from the sensor
            # 1st option for speed reasons since it will be the most likely result
            if(adc_key_in > 60800):
                #print(f"{self.m_pin}.value {adc_key_in} > 60800")
                return VirtualKey.VK_NONE

            #print(f"{self.m_pin}.value => {adc_key_in}")

            if(len(self.m_keys)== 2):
                return getKey2(adc_key_in)
            elif(len(self.m_keys) == 3):
                return getKey3(adc_key_in)
            elif(len(self.m_keys) == 4):
                return getKey4(adc_key_in)
            else:
                pass
                print("KeypadChannel::getKey() wrong m_uKeys")
            return VirtualKey.VK_NONE


    def __init__(self, pin1:AnalogIn, pin2:AnalogIn) -> None:
        '''
        Object initializer
        '''
        # when inactivity timeout will happen
        self.m_iToFireInactivity = 0
        # which channel to use for the next dispatch - index into m_ch
        self.m_iChannel = 0

        # to ensure that multiple keys can be read at the same time...
        self.m_ch = [
            # this reflects Keypad PCB connections
            self.KeypadChannel(pin1, [
                VirtualKey.VK_RIGHT,
                VirtualKey.VK_LEFT,
                VirtualKey.VK_SEL,
                VirtualKey.VK_SOFTA
            ]),
            self.KeypadChannel(pin2, [
                VirtualKey.VK_UP,
                VirtualKey.VK_DOWN,
                VirtualKey.VK_SOFTB
            ])
        ]
        return

    def getAndDispatchKey(self, ulNow: int) -> bool:
        '''
        Call this from the main loop passing to it the result of millis()
        It will call
            onKeyDown(uint8_t vk)
            onKeyAutoRepeat(uint8_t vk)
            onLongKeyDown(uint8_t vk)
            onKeyUp(uint8_t vk)
        Returns: true if key was dispatched and processed
        (then, e.g. screen redraw is needed!), false otherwise.
        '''
        self.m_iChannel += 1
        if(self.m_iChannel >= len(self.m_ch)):
            self.m_iChannel = 0
        if(self.m_iChannel == 0):
            uKeyOtherChannel = self.m_ch[1].m_bOldKey
        else:
            uKeyOtherChannel = self.m_ch[0].m_bOldKey
        return self.m_ch[self.m_iChannel].getAndDispatchKey(
            ulNow, self, uKeyOtherChannel)

    def isUserLongInactive(self, ulNow: int) -> bool:
        return (ulNow > self.m_iToFireInactivity)


    def onUserActivity(self, ulNow: int) -> None:
        '''
        Delay inactivity notification.
        This one is called by KeypadChannel.
        User does NOT have to call it.
        '''
        self.m_iToFireInactivity = ulNow + self.s_iInactivityDelay
        return

    #
    # everything below can be overwritten
    #
    def onUserInActivity(self, ulNow:int) -> bool:
        '''
        Public API callback
        '''
        #print(f"onUserInActivity({ulNow})")
        return False

    def onKeyAutoRepeat(self, vk:VirtualKey) -> bool:
        '''
        Public API callback
        '''
        #print(f"onKeyAutoRepeat({vk})")
        return False

    def onKeyDown(self, vk:VirtualKey) -> bool:
        '''
        Public API callback
        '''
        #print(f"onKeyDown({vk})")
        return False

    def onLongKeyDown(self, vk:VirtualKey) -> bool:
        '''
        Public API callback
        '''
        #print(f"onLongKeyDown({vk})")
        return False

    def onKeyUp(self, vk:VirtualKey) -> bool:
        '''
        Public API callback
        '''
        #print(f"onKeyUp({vk})")
        return False
