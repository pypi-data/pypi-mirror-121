import numpy as np

def mul_reduced(left, coef, factor):
    res = [i for i in left] + [0]
    for i in range(len(left)):
        res[i + 1] += left[i] * coef
    return [i / factor for i in res]

def lagrange_my(x, y):
    M = len(x)
    coefs = [0] * M
    for j in range(M):
        pt = [y[j]]
        for k in range(M):
            if k != j:
                factor = x[j]-x[k]
                pt = mul_reduced(pt, -x[k], factor)
        coefs = np.add(coefs, pt)
    return coefs