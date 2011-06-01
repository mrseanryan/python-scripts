""""
generate_primes.py

from UCD course COMP 41420 by Niall Murphy

May 2011

Note: demonstrates use of the yield keyword, to avoid repeated calculations.
"""

from itertools import count

print __doc__

def generate_primes(stop_at=0):
    primes = []
    for n in count(2):
        if 0 < stop_at < n:
            return # raises the StopIteration exception
        composite = False
        for p in primes:
            if not n % p:
                composite = True
                break
            elif p**2 > n:
                break
        if not composite:
            primes.append(n)
            yield n

for i in generate_primes():
    if i > 100:
        break
    print i
    