from xml.dom.minidom import Document

# Create the minidom document
doc = Document()

# create the Tests container:
tests = doc.createElement("Tests")
doc.appendChild(tests)

#XSL processing instruction:
pi = doc.createProcessingInstruction('xml-stylesheet',
                                     'type="text/xsl" href="testResult.xslt"')
root = doc.firstChild
doc.insertBefore(pi, root)

# add the test tests:
for iResult in range(1,5):
	test = doc.createElement("Test")
	test.setAttribute("id", str(iResult))
	testResult = doc.createElement("Result");
	testResult = "pass";
	if(iResult % 3 == 0):
		testResult = "fail";
	test.setAttribute("result", testResult)
	tests.appendChild(test)

# Print our newly created XML
print doc.toprettyxml(indent="  ")
