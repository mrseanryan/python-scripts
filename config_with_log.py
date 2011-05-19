"""
config.py

Simple code to contain config values.
Logs a warning, when a config value is being over-ridden.

Authors:  Sean Ryan, XiuLi

History:
Created on 18th May 2001
"""

import datetime

class Config:
    def __init__(self):
        self.dictArgToValue = dict()
        self.logFile = open("logs/config.log","rw+")
        self.logFile.seek(0,2) #go to the end of the file
        #TODO make a log class!

    def outputWarning(self, msg):
        #print msg
        now = datetime.datetime.now()
        timeStamp = str(now.year) + " " + str(now.month) + " " + str(now.day)
        timeStamp = timeStamp + " " + str(now.hour) + ":"  + str(now.minute) + "." + str(now.second) + "." + str(now.microsecond) + " - "
        self.logFile.write(timeStamp + msg + "\n")

    def setValue(self, key, val, source):
        if(key in self.dictArgToValue):
            self.outputWarning("config source: " + source + " - value for key " + key + " is being overrided!")
        self.dictArgToValue[key] = val

    def getValue(self, key):
        return self.dictArgToValue[key]

