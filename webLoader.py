"""
Simple py script to load a web server


Author Sean
"""

import os
#import sys
import time

#url = "http://127.0.0.1:8080/"

url = "http://www.yahoo.co.uk"

toExec = "wget " + url

iBatchSize = 1
iBatches = 50

for iBatch in range(iBatches):
    for i in range(iBatchSize):
        os.system(toExec)
    time.sleep(1)

