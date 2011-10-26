from process_text_template import *

# =========== BEGIN CLASSES ==============
# =========== END CLASSES ==============

# =========== BEGIN FUNCTIONS ==============
# =========== END FUNCTIONS ==============

# =========== BEGIN MAIN ==============
varToValue = dict()

#set some values:
varToValue['IRD'] = "20"
varToValue['ProcessingCodes'] = "'18', '20'"
varToValue['ExtraSQLjoin'] = '--my ExtraSQLjoin'

varToValue['ProductType'] = '1'
varToValue['ProcessingTypes'] = "'18', '20'"
varToValue['bHasTimeliness'] = "0"
varToValue['TimelinessInDays'] = "0"
varToValue['bHasApprovalCode'] = "1"
varToValue['CABPrograms'] = "'A001', 'D001'"
varToValue['AcceptanceBrands'] = "'MCC', 'DMC'"

varToValue['RegionAndProductConditions'] = """--template for Region + Product conditions:
		(
			(
			(ab.region in ('A', 'D', 'B', 'E', '1') and ibr.region = 'C') --region
			)
			and 
			(
				(ibr.AcceptanceBrand = 'MCC' and ibr.ProductID in ('MBK', 'MCC', 'MCG', 'MCS', 'MCT', 'MCV', 'MCW', 'MNW', 'MPL', 'MRG', 'MWE') ) -- GCMS Product ID
				or
				(ibr.AcceptanceBrand = 'DMC' and ibr.ProductID in ('MCD', 'MDG', 'MDH', 'MDJ', 'MDO', 'MDP', 'MDR', 'MDS', 'MPG', 'MPP') ) -- GCMS Product ID
			)
		)"""
varToValue['ExtraSQLwhere'] = '--my ExtraSQLwhere'

templateFilePath = "test_data\\templates\\IRD_calculation.template.sql"

outputFilepath = "temp\\IRD_calculation.template.processed.sql"

processTemplate(templateFilePath, varToValue, outputFilepath)

outputFilepathAppended = outputFilepath + ".appended"

outputFilepathInMemory = outputFilepath + ".inMemory"

print "Testing processTemplate()"
processTemplate(templateFilePath, varToValue, outputFilepathAppended)

print "Testing processTemplateAndAppend()"
processTemplateAndAppend(templateFilePath, varToValue, outputFilepathAppended)

print "Testing processTemplateInMemory()"
templateResult = processTemplateInMemory(templateFilePath, varToValue)
templateResultFile = open(outputFilepathInMemory, 'w')
templateResultFile.write(templateResult)
templateResultFile.close()
