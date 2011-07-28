# try out elapsed time output

import time

startTime = time.time()

time.sleep(1)

elapsed = (time.time() - startTime)
print("Time taken: " + str(elapsed) + " seconds")

elapsed = 4650.13599992 

elapsedTime = time.localtime( elapsed )

print ( time.asctime( elapsedTime ) )

dateTimeFormat = '%H hours %M minutes %S seconds'
print("Time taken - formatted: " + time.strftime(dateTimeFormat, elapsedTime))

