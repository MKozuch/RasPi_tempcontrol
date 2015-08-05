#RasPi_tempcontrol

RasPi_tempcontrol.py is a simple script used to control temperature inside Raspberry Pi box case
during hot summer days using a fan.
The fan seed is controlled by Raspberry Pi PWM ouput and temperature is measured by Broadcom
internal sensor.
Every minute the temperature is checked and the fan speed set accordingly. 
Time, temperature and calcuated PWM value are logged to TClog.log file.

NOTE: the fan must NOT be driven directly by GPIO pin, the usage of Darlington pair is suggested.

requires Python3 and wiringpi2 library 
