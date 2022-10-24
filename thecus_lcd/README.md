# Thecus N4810 LCM control
Python script for controlling N4810's front LCD panel

## Usage
1. install pyserial via pip or source code  
2. use code below  
```
from ThecusLCD import ThecusLCD
```
## Examples  
example_testkey.py --> prints out keypresses  
example_testlcd.py --> runs a few function tests  
experiment_sysmon.py --> experimental system monitor script, use with caution !  
  
Install gpiod before running the sysmon script  

## Known issues
Only 'CTRL_LCD' subcommand is available, the MCU doesn't respond to other commands