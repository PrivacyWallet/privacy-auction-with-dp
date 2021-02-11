import dp
import random
from time import time

TIMES = 500

def test(times):
    print("times", times)
    counts = [random.randrange(0,5) for i in range(TIMES)]
    epsilon = [random.randrange(0,1) for i in range(TIMES)]

    start = time()
    dp.count(counts, epsilon)
    end = time()
    print("count", end - start)

    start = time()
    dp.median(counts, epsilon)
    end = time()
    print("median", end - start)

    start = time()
    dp.min(counts, epsilon)
    end = time()
    print("min", end - start)

for i in range(10):
    test(i)
