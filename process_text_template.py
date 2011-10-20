
# =========== BEGIN CLASSES ==============

# =========== END CLASSES ==============

# =========== BEGIN FUNCTIONS ==============

def processLine(line, varToValue):
	processedLine = line
	for var in varToValue:
		processedLine = processedLine.replace('{' + var + '}', varToValue[var])
	return processedLine

def processTemplate(templateFilePath, varToValue, outputFilepath):
	templateFile = open(templateFilePath, 'r')
	
	outputFile = open(outputFilepath, 'w')
	
	for line in templateFile:
		processedLine = processLine(line, varToValue)
		outputFile.write(processedLine)
		#outputFile.write('\n')
	
	templateFile.close()
	outputFile.close()

# =========== END FUNCTIONS ==============

# =========== NO MAIN ==============
