# N4810/N2810 patched ITE IT8616 driver
This is a patched version of it87 SuperIO chip driver based on Thecus' kernel source patches  
Thecus uses a SuperIO IC that's not supported by the in-tree it87 kernel driver(IT8616E), so patching is needed  

## Functions
- Patched using the latest upstream source
- Modified to make Power LED control available via /proc/hwm interface
- Name changed to thecus_it87 to prevent collision with in-tree driver

## Build
install dkms first (build tools should also be installed)
```
make clean
make dkms
```
## Usage
Monitoring and fan control can be carried out using lm-sensors 
- The fan of N4810 is at fan2/pwm2
- The fan of N2810 should also be at fan2/pwm2 (not tested)

Power LED control can be carried out using the below command
```
echo "SLED a b c" > /proc/hwm
```
a:  
1 ==> read status  
2 ==> control LED  
	
b:  
0 ==> blue LED  
1 ==> red LED  

c:  
0 ==> off  
1 ==> on  
2 ==> blink  

## Known issues
- When the driver loads, blue LED defaults to blinking
- When building on Proxmox VE, pve-headers should be reinstalled everytime before building