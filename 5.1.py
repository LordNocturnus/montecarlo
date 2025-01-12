import numpy as np
import math


def moment_func(k = 1, l = 0.2, mu = 0.25, sigma = 0.05):
    if k== 0:
        return
    return np.exp(
        -l * k * mu + 0.5 * l**2 * k**2 * sigma**2
    )

def binomial_prob(k, n, p = moment_func(1)):
    return math.comb(n, k) * p**k * (1-p)**(n-k)

def prob_i_minus_one(i):
    if i ==1:
        return 1 - moment_func(1)
    return moment_func(i-1) * (1 - moment_func(1)) + moment_func(1) * prob_i_minus_one(i-1)


# print(moment_func(1))
for n in range(3, 10):
    # for m in range(n-1, n+1):
    m = n-1
    p_actual = prob_i_minus_one(n)
    p_approx = binomial_prob(m, n=n)
    error = np.abs(p_actual - p_approx)
    error_rel = error / p_actual

    print(prob_i_minus_one(n))
    print(binomial_prob(m, n=n))
    print(error_rel)
    print('(n,m) = ({}, {})'.format(n, m))

    m=n
    p_actual = moment_func(m)
    p_approx = binomial_prob(m, n=n)
    error = np.abs(p_actual - p_approx)
    error_rel = error / p_actual
    print(moment_func(m))
    print(binomial_prob(m, n=n))
    print(error_rel)
    print('(n,m) = ({}, {})'.format(n, m))