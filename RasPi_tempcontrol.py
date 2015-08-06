#!/usr/bin/env python3

import subprocess
import wiringpi2
import time
import csv
import os.path


class TempControl:
    PWMmode = False
    fanRunning = False 

    def init(self, PWMmode):
        self.PWMmode = PWMmode
        wiringpi2.wiringPiSetup()
        if self.PWMmode == True:
          wiringpi2.pinMode(1, 2)
        else:
          wiringpi2.pinMode(1,1)
     
        
    @staticmethod
    def readtemp():
        command = '/opt/vc/bin/vcgencmd measure_temp'
        tmp = subprocess.check_output(command, shell=1)
        tmp = tmp.decode("utf-8")
        tempVal = float(tmp[-7:-3])
        return(tempVal)
        
        
    def setFanSpeed(self):
        START = 650      #  this value is minimal pwm value that can start the fan, depends on the fan and transistors used
        LO_TEMP = 45.0   #  minimal temperature that turns on the fan 
        HI_TEMP = 55.0   #  when core temperature is higher than this the fan operates at full speed
        tempDiff = HI_TEMP - LO_TEMP
        
        temp = self.readtemp()

        if self.PWMmode:                                
          if temp < LO_TEMP:
              pwm = 0
          elif temp > HI_TEMP:
              pwm = 1023
          else:        
              pwm = (1023-START)/tempDiff * temp - ((1023-START)/tempDiff)*LO_TEMP + START
              pwm = int(pwm)
          wiringpi2.pwmWrite(1, pwm)
          return pwm
        
        elif not self.PWMmode:
          if self.fanRunning:
            if temp <= LO_TEMP:
              wiringpi2.digitalWrite(1, 0)
              self.fanRunning = False
              return(0)
            else: return(1023)
          elif not self.fanRunning:
            if temp > HI_TEMP:
              wiringpi2.digitalWrite(1, 1)
              self.fanRunning = True
              return(1023)
            else: return(0)
              
        
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
    import sys
    try:
      mode = sys.argv[sys.argv.index('-m') + 1]
      if mode == 'pwm':  pwmMode = True
      else:  pwmMode = False
    except(IndexError, ValueError):
      pwmMode = False
    tc = TempControl()
    tc.init(pwmMode)
    #print('initialised in PWM mode: {}'.format(pwmMode))
    logFileName = 'TClog.log'
    while True:
        pwm = tc.setFanSpeed()
        #print("current temp is {}'C".format(TempControl().readtemp()))
        #print("fan spped set to {}".format(pwm))
        TempControl.logtemp(logFileName, TempControl.readtemp(), pwm)
        time.sleep(30) 

