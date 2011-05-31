import os

bad_checkin_line = "(rank,m[0],l[1],l["

filename = "ChessBoard.py"

iStartRev = 5
iEndRev = 23

def checkDiffRange(iFromRev, iToRev):
	svnGetArgs = "diff -r" + str(iFromRev) + ":" + str(iToRev) + " " + filename
	toExec = "svn " + svnGetArgs

	p = os.popen(toExec,"r")
	while 1:
		line = p.readline()
		if not line: break
		#print " >> " + line
		if bad_checkin_line in line:
			return True
	return False

def bSearchDiff(iStartRev, iEndRev):
	print "bSearchDiff " + str(iStartRev) + ":" + str(iEndRev)
	bFound = checkDiffRange(iStartRev, iEndRev)
	if(bFound):
		if(iStartRev == iEndRev - 1):
			print "!!! FOUND !!! rev: " + str(iEndRev)
		else:  
			iMid = iStartRev + (iEndRev - iStartRev) / 2
			if(not bSearchDiff(iStartRev, iMid)):
				bSearchDiff(iMid, iEndRev)
	return bFound

bFound = bSearchDiff(iStartRev, iEndRev)

#for iRev in range(iRevsToCheck):
#	iFromRev = iRev + iStartRev
#	iToRev = iRev + iStartRev + 1
	#bFound = findStringInRevRange(

