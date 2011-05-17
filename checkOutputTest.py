"""
checkOutputTest.py

This is a unit test to test the output of the netcat application.

Authors:  Sean Ryan, XiuLi

History:
Created on 17th May 2001
"""

import os
import subprocess
import time
import unittest
import sys

class CheckOutputTest(unittest.TestCase):
    """
    This is a unit test to test the output of the netcat application.
    """

    def setUp(self):
        pathToNetCat = ""

    def runExeAndGetOutput(self, exe, args):
        """
        runs the given exe, with the given args.  Captures stdout + stderr, and returns in a string.
        """

        print "running: " + exe + " '"  +str(args) + "'"

        exe = exe + ' ' + str(args)
        process = subprocess.Popen(exe, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        (stdout_cap, stderr_cap) = process.communicate()

        print "captured! " + stderr_cap

        return (stdout_cap, stderr_cap)

    def testRunNetCat(self):
        print "testRunNetCat()"
        (stdout_cap, stderr_cap) = self.runExeAndGetOutput("nc", '-v -w 2 -z 127.0.0.1 20-30')

        #read in file with the expected results:
        knownGoodFile = open('known_good_output.txt', 'r')
        knownGoodOutput = ""
        for line in knownGoodFile:
            knownGoodOutput += line

        self.assertEqual(knownGoodOutput, stderr_cap)

def suite():
    mySuite = unittest.TestSuite()
    #please add your tests here!
    mySuite.addTest(unittest.makeSuite(CheckOutputTest))
    return mySuite

suiteToTest = suite()
unittest.TextTestRunner(verbosity=2).run(suiteToTest)

