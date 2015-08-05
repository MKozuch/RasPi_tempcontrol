#!/usr/bin/env python3

import subprocess
import wiringpi2
import time
import csv
import os.path


class TempControl:

    def init(self):
        wiringpi2.wiringPiSetup()
        wiringpi2.pinMode(1, 2)
        
    @staticmethod
    def readtemp():
        command = '/opt/vc/bin/vcgencmd measure_temp'
        tmp = subprocess.check_output(command, shell=1)
        tmp = tmp.decode("utf-8")
        tempVal = float(tmp[-7:-3])
        return(tempVal)
        
    def setFanSpeed(self):
        START = 650      #  this value is minimal pwm value that can start the fan, depends on the fan and used transistors
        LO_TEMP = 45.0   #  minimal temperature that turns on the fan 
        HI_TEMP = 55.0   #  when core temperature is higher than this the fan operates at full speed
        tempDiff = HI_TEMP - LO_TEMP
                                
        temp = self.readtemp()
        if temp < LO_TEMP:
            pwm = 0
        elif temp > HI_TEMP:
            pwm = 1023
        else:        
            pwm = (1023-START)/tempDiff * temp - ((1023-START)/tempDiff)*LO_TEMP + START
            pwm = int(pwm)
        wiringpi2.pwmWrite(1, pwm)
        return pwm
        
    @staticmethod
    def logtemp(filename, temp, pwmValue):
        logFileExist = os.path.isfile(filename)
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        with open(filename, 'a', newline='\n') as logfile:
            fileWriter = csv.writer(logfile, delimiter='\t')
            if not logFileExist:
                fileWriter.writerow(('Timestamp', 'Core temperature[*C]', 'PWM Value'))
            fileWriter.writerow((timestamp, temp, pwmValue)) 
        
        
if __name__ == "__main__":
    TempControl().init()
    logFileName = 'TClog.log'
    while True:
        pwm = TempControl().setFanSpeed()
        #print("current temp is {}'C".format(TempControl().readtemp()))
        #print("fan spped set to {}".format(pwm))
        TempControl.logtemp(logFileName, TempControl.readtemp(), pwm)
        time.sleep(60) 

