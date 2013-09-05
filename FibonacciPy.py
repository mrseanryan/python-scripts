print('FibonacciPy')

valNless1 = 1
valNless2 = 0

def fiboNext(valNless1, valNless2):
    valN = valNless1 + valNless2

    valNless2 = valNless1
    valNless1 = valN

    return (valN, valNless1, valNless2)

#we use a loop, instead of recursion, to avoid possible stack overflow (if count very large)
def fiboSeries(count, valNless1, valNless2):
    count = count - 2 #the first 2 entries have already been output
    while(count > 0):
        (valN, valNless1, valNless2) = fiboNext(valNless1, valNless2)
        print(valN)
        count = count - 1

#print the first 2 entries in the sequence:
print(valNless2)
print(valNless1)

count = 100

#generate the rest of the sequence:
fiboSeries(count, valNless1, valNless2)
