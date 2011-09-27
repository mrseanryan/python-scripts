#rough script to generate SQL field names
#
#just to save some typing ...

for i in range(1,75 + 1): #1..75
	print "@Field " + str(i) + " as Field" + str(i) + ","
