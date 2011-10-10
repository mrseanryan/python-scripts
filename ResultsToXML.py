from ResultsToXML import *

# =========== BEGIN CLASSES ==============
# =========== END CLASSES ==============

# =========== BEGIN FUNCTIONS ==============
# =========== END FUNCTIONS ==============

# =========== BEGIN MAIN ==============
IRDtestResults = list()

irdNames = ['20', '75', '85']

#build the collection of IRD results:
for iTestId in range(1,10+1):
	IRD = irdNames[iTestId % len(irdNames)]
	bIsPass = True
	if(iTestId % 3 == 0):
		bIsPass = False;
	
	result = IRDTestResult(iTestId, IRD, bIsPass)
	IRDtestResults.append(result)

#create the XML:
xmlDoc = createXML(IRDtestResults)

print xmlDocToString(xmlDoc)
# =========== END MAIN ==============
