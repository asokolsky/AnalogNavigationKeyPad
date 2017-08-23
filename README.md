# Analog Navigation KeyPad Library

Simple analog keypad designed to recognize simultaneous button presses.
Has a central 5-way joystick and two (left and right) buttons.

## Hardware

[Schematics and PCB] (https://easyeda.com/asokolsky/Analog_Navigation_Keypad-a25307c2a2254b4eb4a9cd3543392b90)
[Schematics and PCB for SMD Version] (https://easyeda.com/asokolsky/Analog_Navigation_Keypad_copy-e961efefbccf49cd99776f7c87a63a96)

### PinOut

| Pin | Name | Description |
| --- | -----| -----|
|1|VCC| Voltage supply.  Connect to VCC of your controller.|	
|2|A1| Connect to analog input of your controller.|
|3|A2| Connect to another analog input of your controller.|
|4|NC| Not connected.|
|5|AGND| Analog Ground or just Ground|

## Software Samples

AnalogNavigationKeyPad.ino

## Sequence of CallBacks 

### Single Button presses

~~~~
MyNavKeyPad::onKeyDown vks=VK_SOFTA 
MyNavKeyPad::onKeyUp vks=VK_SOFTA 
~~~~

### First one then another button being pressed

~~~~
MyNavKeyPad::onKeyDown vks=VK_SOFTA 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA 
MyNavKeyPad::onKeyDown vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onLongKeyDown vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyAutoRepeat vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyUp vks=VK_SOFTA VK_SOFTB 
MyNavKeyPad::onKeyUp vks=VK_SOFTB 
~~~~



