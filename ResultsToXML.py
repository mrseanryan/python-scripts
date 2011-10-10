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
		test.setAttribute("id", str(irdResult.TestId).lower())
		test.setAttribute("IRD", irdResult.IRD)
		
		if not irdResult.IRD in IRDs:
			IRDs.append(irdResult.IRD)
		
		if(not irdResult.bIsPass):
			if not irdResult.IRD in failedIRDs:
				failedIRDs.append(irdResult.IRD)
		test.setAttribute("pass", str(irdResult.bIsPass).lower())
		tests.appendChild(test)

	IRDs.sort()
	failedIRDs.sort()
	
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
		irdNode.setAttribute("pass", str(bSuccess).lower())
	
	return doc

def xmlDocToString(xmlDoc):
	return xmlDoc.toprettyxml(indent="  ")

# =========== END FUNCTIONS ==============

# =========== NO MAIN ==============
