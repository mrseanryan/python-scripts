
# =========== BEGIN CLASSES ==============

# =========== END CLASSES ==============

# =========== BEGIN FUNCTIONS ==============

def processLine(line, varToValue):
	processedLine = line
	for var in varToValue:
		processedLine = processedLine.replace('{' + var + '}', varToValue[var])
	return processedLine

def processTemplateAndAppend(templateFilePath, varToValue, outputFilepath):
	processTemplateImpl(templateFilePath, varToValue, outputFilepath, True)

def processTemplate(templateFilePath, varToValue, outputFilepath):
	processTemplateImpl(templateFilePath, varToValue, outputFilepath, False)

def processTemplateInMemory(templateFilePath, varToValue):
	processedResult = ""
	
	templateFile = open(templateFilePath, 'r')
	
	for line in templateFile:
		processedResult = processedResult + processLine(line, varToValue)
	templateFile.close()
	return processedResult

def processTemplateImpl(templateFilePath, varToValue, outputFilepath, bAppend):

	
	outFileMode = 'w'
	if bAppend:
		outFileMode = 'a'
	outputFile = open(outputFilepath, outFileMode)
	
	templateResult = processTemplateInMemory(templateFilePath, varToValue)
	
	for line in templateResult:
		processedLine = processLine(line, varToValue)
		outputFile.write(processedLine)
		#outputFile.write('\n')
	
	outputFile.close()

# =========== END FUNCTIONS ==============

# =========== NO MAIN ==============
