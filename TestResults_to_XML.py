from xml.dom.minidom import Document


# =========== BEGIN CLASSES ==============
class IRDTestResult:
	def __init__(self, TestId, IRD, bIsPass):
		self.TestId = TestId
		self.IRD = IRD
		self.bIsPass = bIsPass
# =========== END CLASSES ==============

# =========== BEGIN FUNCTIONS ==============
def createXML(IRDtestResults):

	# Create the minidom document
	doc = Document()

	# create the Tests container:
	root = doc.createElement("IRDTests")
	doc.appendChild(root)
	
	#XSL processing instruction:
	pi = doc.createProcessingInstruction('xml-stylesheet',
										 'type="text/xsl" href="testResult.xslt"')
	root = doc.firstChild
	doc.insertBefore(pi, root)

	IRDs = list()
	failedIRDs = list()
	
	# add the test results:
	tests = doc.createElement("Tests")
	root.appendChild(tests)
	for irdResult in IRDtestResults:
		test = doc.createElement("Test")
		test.setAttribute("id", str(irdResult.TestId))
		test.setAttribute("IRD", irdResult.IRD)
		
		if not irdResult.IRD in IRDs:
			IRDs.append(irdResult.IRD)
		
		testResult = doc.createElement("Result")
		testResult = "pass"
		if(not irdResult.bIsPass):
			testResult = "fail"
			if not irdResult.IRD in failedIRDs:
				failedIRDs.append(irdResult.IRD)
		test.setAttribute("result", testResult)
		tests.appendChild(test)

	#add summary of IRDs:
	IRDsNode = doc.createElement("IRDs")
	root.appendChild(IRDsNode)
	for IRD in IRDs:
		irdNode = doc.createElement("IRD")
		IRDsNode.appendChild(irdNode)
		irdNode.setAttribute("name", IRD)
		bSuccess = True
		if IRD in failedIRDs:
			bSuccess = False
		irdNode.setAttribute("pass", str(bSuccess))
	
	return doc

def xmlDocToString(xmlDoc):
	return xmlDoc.toprettyxml(indent="  ")

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
