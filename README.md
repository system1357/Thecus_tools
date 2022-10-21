# Thecus N2810/N4810 Tools
A collection of scripts and drivers for Thecus Linux-based NAS devices

## Intro
thecus_it87:  
Patched it87 SuperIO chip driver found in Thecus' kernel source  
  
thecus_lcd:  
Python script for controlling N4810's front LCD panel  
  
## Tips
### 1. GPIO:  
N4810 has 4 red HDD error LEDs and two USB status LEDs all wired to gpiochip1  
N2810/Pro/Plus has identical arrangements, but only 2 HDD error LEDs(HDD0, HDD1) and a diffrent USB Green LED
- HDD0: GPIO 0
- HDD1: GPIO 3
- HDD2: GPIO 7
- HDD3: GPIO 1
- USB Green(N4810): GPIO 6
- USB Green(N2810): GPIO 18
- USB Red: GPIO 8  

The leds can be controlled via gpioset:  
```
gpioset 1 a=b
```  
a: GPIO pin  
b: state(0=on, 1=off)  

### 2. lm-sensors  
Pwmconfig can detect all inputs and outputs normally, but the script will think pwm2 and pwm3 both control the fan(which is actually pwm2 only)  
Manually fixing the config file(/etc/fancontrol) is needed