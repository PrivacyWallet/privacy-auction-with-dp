import dp
import random
from time import time

TIMES = 500

def test():
    counts = [random.randrange(0,5) for i in range(TIMES)]
    epsilon = [random.randrange(0,1) for i in range(TIMES)]

    start = time()
    dp.count(counts, epsilon)
    end = time()
    print(end - start)

for i in range(10):
    test()
