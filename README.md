#RasPi_tempcontrol

RasPi_tempcontrol.py is a simple script used to control temperature inside Raspberry Pi box case
during hot summer days using a fan.

The fan seed is controlled by Raspberry Pi PWM ouput and temperature is measured by Broadcom chip
internal sensor.
Every minute the temperature is checked and the fan speed set accordingly. 
Time, temperature and calcuated PWM value are logged to TClog.log file.

NOTE: the fan must NOT be driven directly by GPIO pin, the usage of Darlington pair is suggested.

NOTE: pin 1 (BCM_GPIO 18) is shared with RasPi audio system, that means that it is not possible to use both 3.5mm 
audio jack output and PWM driving at the same time
In order to addressthis issue digital mode has been implemented, running script with option '-m pwm/digital' allows to select 
either linear or digital fan speed control

Requires Python3 and wiringpi2 library 
