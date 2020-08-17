import cvxpy as cp
import numpy as np
from random import randint

UPPER_BOUND = 1e7

# number data owner 
NUMBER = 3

psi_vec = [randint(0, UPPER_BOUND) for _ in range(NUMBER)]

# budget
B = cp.Parameter(value=2*UPPER_BOUND)
theta_vec = cp.Variable(NUMBER)
epsilon_vec = [randint(0, UPPER_BOUND)/UPPER_BOUND for _ in range(NUMBER)]
epsilon_vec = cp.Parameter(NUMBER, value=epsilon_vec)

print(f"{theta_vec=}")
print(f"{epsilon_vec=}")

# Create two scalar optimization variables.

# Create two constraints.
constraints = [0 <= theta_vec, theta_vec <= 1, cp.sum_squares(theta_vec) <= B]

# Form objective.
obj = cp.Maximize(cp.sum(theta_vec * epsilon_vec))

# Form and solve problem.
prob = cp.Problem(obj, constraints)
prob.solve()  # Returns the optimal value.
print("status:", prob.status)
print("optimal value", prob.value)
print("varepsilon:", [i.value for i in epsilon_vec])

# retrans
theta_vec = [i.value for i in theta_vec]
epsilon_vec = [i.value for i in epsilon_vec]

print("theta", theta_vec)
pairs = list(zip(psi_vec, theta_vec))
print(pairs)

print("constrants:", sum([i*i for i in theta_vec]))
print("theta / epsilon", [theta_vec[i] / epsilon_vec[i] for i in range(len(epsilon_vec))])
print(["buy" if x <= y else "skip"for x, y in pairs])
print(sum([x if x <= y else 0 for x, y in pairs]))

