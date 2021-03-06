from temp import NS1, NS2, NS3, NL1, NL2, NL3, NH1, NH2, NH3, objective1
from GivenProb import NH, NL, NS, objective

import numpy as np

def functest(x, func, *location):
    out = np.zeros(len(x))
    for i in range(len(x)):
        out[i] = func(x[i], *location)
    return out


np.random.seed(42)
test = np.random.rand(100,10)
print(functest(test, NH, 0)) #np.set_printoptions(suppress=True)
print(functest(test, NH, 1))
print(functest(test, NH, 2))
print(functest(test, NL, 0))
print(functest(test, NL, 1))
print(functest(test, NL, 2))
print(functest(test, NS, 0))
print(functest(test, NS, 1))
print(functest(test, NS, 2))
print(functest(test, objective))

print(functest(test, NH1))
print(functest(test, NH2))
print(functest(test, NH3))
print(functest(test, NL1))
print(functest(test, NL2))
print(functest(test, NL3))
print(functest(test, NS1)) 
print(functest(test, NS2))
print(functest(test, NS3))
print(functest(test, objective1))

sum(functest(test, NH, 0) == functest(test, NH1)) == 100
sum(functest(test, NH, 1) == functest(test, NH2)) == 100
sum(functest(test, NH, 2) == functest(test, NH3)) == 100
sum(functest(test, NL, 0) == functest(test, NL1)) == 100
sum(functest(test, NL, 1) == functest(test, NL2)) == 100
sum(functest(test, NL, 2) == functest(test, NL3)) == 100
sum(functest(test, NS, 0) == functest(test, NS1)) == 100
sum(functest(test, NS, 1) == functest(test, NS2)) == 100
sum(functest(test, NS, 2) == functest(test, NS3)) == 100
sum(functest(test, objective) == functest(test, objective)) == 100
