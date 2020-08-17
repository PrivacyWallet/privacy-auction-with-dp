from typing import List, Tuple
from math import sqrt
from random import random, randint
import pytest
import cvxpy as cp

EPSILON = 1e-9
ROUND_EPSILON = 7
ASSERT_EPSILON = 5e-3
TEST_REPEAT_TIMES = 10
UPPER_BOUND = 1e7


def sum_of_square(vec: List[int]) -> int:
    return sum(i * i for i in vec)


def original_optimize(epsilon_vec: List[int], B: int) -> Tuple[int, List[int]]:
    B = cp.Parameter(value=B)
    theta_vec = cp.Variable(len(epsilon_vec))
    epsilon_vec = cp.Parameter(len(epsilon_vec), value=epsilon_vec)

    constraints = [0 <= theta_vec, theta_vec <=
                   1 * UPPER_BOUND, cp.sum_squares(theta_vec) <= B]
    obj = cp.Maximize(cp.sum(theta_vec * epsilon_vec))
    prob = cp.Problem(obj, constraints)
    prob.solve()  # Returns the optimal value.
    return [prob.value, [i.value for i in theta_vec]]


def optimize(epsilon_vec: List[int], B: int) -> Tuple[int, List[int]]:

    pass


# def _optimize(epsilon_vec: List[int], B: int) -> List[int]:
    # # only decend data available
    # if len(epsilon_vec) < B:
        # return [1] * len(epsilon_vec)
    # if sum_of_square([i / epsilon_vec[0] for i in epsilon_vec]) > B:
        # lower, upper = 0, 1 / epsilon_vec[0]
        # while upper - lower > EPSILON:
            # mid = (upper + lower) / 2
            # l = [mid * i for i in epsilon_vec]
            # if sum_of_square(l) >= B:
                # upper = mid
            # else:
                # lower = mid
        # return l
    # B = B - 1
    # return [1, *_optimize(epsilon_vec[1:], B)]

# heavily optimized algorithm
def _optimize(epsilon_vec: List[int], B: int) -> List[int]:
    print(f"Get epsilon_vec: {epsilon_vec}")
    print(f"Get Budget: {B}")
    
    sum_of_squre_vec = [1] * len(epsilon_vec)
    sum_of_squre_vec[-1] = 1 * UPPER_BOUND**2
    # print(f"{sum_of_squre_vec=}")
    for i in range(len(epsilon_vec)-2,-1,-1):
        sum_of_squre_vec[i] = (((sum_of_squre_vec[i+1]) * epsilon_vec[i+1]**2 / epsilon_vec[i]**2) + UPPER_BOUND**2) 
    print("sum of square vec")
    print(sum_of_squre_vec)

    theta_vec = []

    while len(epsilon_vec) > 0:
        print(theta_vec)
        if len(epsilon_vec) * UPPER_BOUND**2 < B:
            theta_vec.extend([1 * UPPER_BOUND] * len(epsilon_vec))
            break
        # if sum_of_square([i/epsilon_vec[0] for i in epsilon_vec]) > B:
        if sum_of_squre_vec[0] > B:
            print(f"{B=}, {sum_of_squre_vec[0]=}, {epsilon_vec[0]=}")
            factor = sqrt(B / (sum_of_squre_vec[0] * epsilon_vec[0]**2))
            
            theta_vec.extend([UPPER_BOUND *i*factor for i in epsilon_vec])
            break
        B = B - 1 * UPPER_BOUND
        theta_vec.append(1 * UPPER_BOUND )
        epsilon_vec = epsilon_vec[1:]
        sum_of_squre_vec = sum_of_squre_vec[1:]

    return theta_vec


# unit test

def test_sum_of_square():
    assert sum_of_square([1, 2, 3]) == 14


def test_origin_optimize():
    B = random() * 100
    eps_vec = [random() for _ in range(10)]
    eps_vec.sort(reverse=True)

    _, origin_vec = original_optimize(eps_vec, B)

    assert sum_of_square(origin_vec) < B + ASSERT_EPSILON
    for i in origin_vec:
        assert 0 <= round(i, ROUND_EPSILON) <= UPPER_BOUND


def test_sorted_optimize_func_simple():
    # assert _optimize([5.9928756509742485, 3.729049949676304, 1.1981916388015845]
# , 3.71011037080302) == [1]*3

    B = random()
    ans = _optimize([1, 1], B)
    for i in ans:
        assert abs(i - sqrt(B/2)) < EPSILON


def test_sorted_optimize_func_certain():

    B = 1.3440638268820637
    eps_vec = [0.8533991519326575, 0.6238007131912048]
    eps_vec.sort(reverse=True)

    origin_optimized, origin_vec = original_optimize(eps_vec, B)
    vec = _optimize(eps_vec, B)
    print(f"{B=}")
    print(f"{eps_vec=}")
    optimized = sum([x*y for x, y in zip(eps_vec, vec)])
    print(f"{origin_optimized=}, {optimized=}")
    print(origin_optimized - optimized)
    print(f"{origin_vec=}")
    print(f"{vec=}")
    for i in range(len(vec)):
        assert abs(vec[i] - origin_vec[i]) < ASSERT_EPSILON


@pytest.mark.repeat(TEST_REPEAT_TIMES)
def test_sorted_optimize_func_random():

    B = random() * 50
    eps_vec = [random()*UPPER_BOUND for _ in range(randint(1, 30))]
    eps_vec.sort(reverse=True)

    print(f"{B=}")
    print(f"{eps_vec=}")
    origin_optimized, origin_vec = original_optimize(eps_vec, B)
    vec = _optimize(eps_vec, B)
    optimized = sum([x*y for x, y in zip(eps_vec, vec)])
    print(f"{origin_optimized=}, {optimized=}")
    print(origin_optimized - optimized)
    print(f"{origin_vec=}")
    print(f"{vec=}")
    for i in range(len(vec)):
        assert abs(vec[i] - origin_vec[i]) < ASSERT_EPSILON
    assert round(optimized, 7) >= round(origin_optimized, 7) \
            or sum_of_square(origin_vec) > B


@pytest.mark.repeat(TEST_REPEAT_TIMES)
def test_sorted_optimize_func_random_large_set():

    B = random() * 2000
    eps_vec = [random() for _ in range(randint(1, 10000))]
    eps_vec.sort(reverse=True)

    print(f"{B=}")
    print(f"{eps_vec=}")
    origin_optimized, origin_vec = original_optimize(eps_vec, B)
    vec = _optimize(eps_vec, B)
    optimized = sum([x*y for x, y in zip(eps_vec, vec)])
    print(f"{origin_optimized=}, {optimized=}")
    print(origin_optimized - optimized)
    print(f"{origin_vec=}")
    print(f"{vec=}")
    # for i in range(len(vec)):
    # assert abs(vec[i] - origin_vec[i]) < ASSERT_EPSILON
    assert round(optimized, ROUND_EPSILON) >= round(origin_optimized,
                                                    ROUND_EPSILON) \
        or abs(origin_optimized - optimized) < ASSERT_EPSILON \
        or sum_of_square(origin_vec) > B

if __name__ == "__main__":
    from pprint import pprint as print
    a = [0.1, 0.3, 0.5, 0.7, 0.9]
    a.sort(reverse=True)
    print(original_optimize([i*UPPER_BOUND for i in a], 1.2*UPPER_BOUND))
    import pdb
    pdb.set_trace()
    print(_optimize([i*UPPER_BOUND for i in a], 1.2*UPPER_BOUND))


    # print(original_optimize(a, 2))
