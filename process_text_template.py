
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

def processTemplateImpl(templateFilePath, varToValue, outputFilepath, bAppend):
	templateFile = open(templateFilePath, 'r')
	
	outFileMode = 'w'
	if bAppend:
		outFileMode = 'a'
	outputFile = open(outputFilepath, outFileMode)
	
	for line in templateFile:
		processedLine = processLine(line, varToValue)
		outputFile.write(processedLine)
		#outputFile.write('\n')
	
	templateFile.close()
	outputFile.close()

# =========== END FUNCTIONS ==============

# =========== NO MAIN ==============
