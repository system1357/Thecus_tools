# Thecus N2810/N4810 Tools
A collection of scripts and drivers for Thecus Linux-based NAS devices

## thecus_it87
Patched it87 SuperIO chip driver found in Thecus' kernel source

## thecus_lcd
Python script for controlling N4810's front LCD panel

## Tips
1. GPIO: N4810 has 4 red HDD error LEDs and two USB status LEDs
    - HDD0: GPIO 853
    - HDD1: GPIO 856
    - HDD2: GPIO 860
    - HDD3: GPIO 854
    - USB Green: GPIO 859
    - USB Red: GPIO 861
   all LEDs are active-low, means you have to echo 0 to turn it on
2. lm-sensors
   Pwmconfig can detect all inputs and outputs normally, but the script will think pwm2 and pwm3 both control the fan(which is actually pwm2 only)
   Manually fixing the config file(/etc/fancontrol) should fix this