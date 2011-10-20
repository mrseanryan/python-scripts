from process_text_template import *

# =========== BEGIN CLASSES ==============
# =========== END CLASSES ==============

# =========== BEGIN FUNCTIONS ==============
# =========== END FUNCTIONS ==============

# =========== BEGIN MAIN ==============
varToValue = dict()



templateFilePath = "test_data\templates\IRD_calculation.template.sql"

outputFilepath = "temp\IRD_calculation.template.processed.sql"

processTemplate(templateFilePath, varToValue, outputFilepath)
