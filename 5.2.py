# import sympy as sp
#
# # Define the symbols
# lambda_ = sp.symbols('lambda')
# mu = sp.symbols('mu')
#
# # Define the matrix
# matrix = sp.Matrix([
#     [-lambda_, lambda_, 0, 0, 0],
#     [mu, -mu - lambda_, lambda_, 0, 0],
#     [0, 2 * mu, -2 * mu - lambda_, lambda_, 0],
#     [0, 0, 2 * mu, -2 * mu - lambda_, lambda_],
#     [0, 0, 0, 2 * mu, -2 * mu]
# ])
# matrix = matrix.T
#
# sol, _ = matrix.gauss_jordan_solve(sp.Matrix([0, 0, 0, 0, 0]))
# sp.simplify(sol)
# print(sol)
# print((sol.T @ matrix.T).evalf(subs={lambda_:3.0, mu:2.0}))

import numpy as np

lamb = 3
mu = 2
rho = lamb / 2 / mu

pi = np.array([
    2, rho, rho**2, rho**3, rho**4
])
pi = pi / sum(pi)

vi = np.array([
    lamb, mu+lamb, 2*mu+lamb, 2*mu+lamb, 2*mu
])

Pij = np.zeros((5,5))
Pij[0, 1] = 1
Pij[1, 2] = lamb / (mu+lamb)
Pij[2, 3] = lamb / (2*mu+lamb)
Pij[3, 4] = lamb / (2*mu+lamb)
Pij[1, 0] = mu / (mu+lamb)
Pij[2, 1] = 2*mu / (2*mu+lamb)
Pij[3, 2] = 2*mu / (2*mu+lamb)
Pij[4, 3] = 1

ci = np.zeros(5)
ci[3] = 1
ci[4] = 2

cij = np.zeros((5, 5))
# for i in range(4):
for i in [2, 3]:
    cij[i, i+1] = 1

num = ci @ pi

# den1 = vi @ pis)@pi)
# print(den1)
# print(den2)
# print(den1*den2)

den = sum(np.sum(cij * Pij, axis=1)*pi*vi)
print(den)
print(num / den)
