import numpy as np 
from scipy.optimize import minimize
from scipy.stats import  expon

lambdaB = 1 #Buyer's exponential distribution parameter
lambdaS = 1 #Seller's exponential distribution parameter
dist = 2
s = 100


def CDF(x, parameter):
    return expon.cdf(x, scale = 1/parameter)

def PDF(x, parameter):
    return expon.pdf(x, scale = 1/parameter)

def objective(x):
    r = x[6] 
    PL = [x[0], x[1], x[2]]
    PH = [x[3], x[4], x[5]]
    location = [0,1,2]
    output = 0
    for i in location:
        output = output + r*(NL(x, i)*PL[i] + NH(x, i)*PH[i])
    return -output

def NH(x, location):
    return 1-CDF((x[3+location]-x[0+location])/(x[7+location]), lambdaB)
        
def NL(x, location):
    return CDF((x[3+location]-x[0+location])/x[7+location], lambdaB) - CDF((s-x[0+location])/(1+x[7+location]), lambdaB)

def NS(x, location):
    return 1- CDF(
            (NH(x, location)*(x[3+location]-x[6])+NL(x, location)*(x[location]-x[6]))
            /(NH(x, location) + (1-x[7+ location])*NL(x, location)+2*x[7+location]*NL(x, location))
            , lambdaS)

def constraintGenEq1(x, location = 0):
    return NS(x, location)- NH(x, location) -(1+x[7+location])*NL(x, location)
def constraintGenEq2(x, location = 1):
    return NS(x, location)- NH(x, location) -(1+x[7+location])*NL(x, location)
def constraintGenEq3(x, location = 2):
    return NS(x, location)- NH(x, location) -(1+x[7+location])*NL(x, location)

def constraintProbLow1(x):
    return x[7] - (x[3]-x[0])/(dist) 
def constraintProbLow2(x):
    return x[8] - (x[4]-x[1])/(dist) 
def constraintProbLow3(x):
    return x[9] - (x[5]-x[2])/(dist) 

conGen1= {'type': 'eq', 'fun': constraintGenEq1} 
conGen2= {'type': 'eq', 'fun': constraintGenEq2}
conGen3= {'type': 'eq', 'fun': constraintGenEq2}
conProb1= {'type': 'ineq', 'fun': constraintProbLow1}
conProb2= {'type': 'ineq', 'fun': constraintProbLow2}
conProb3= {'type': 'ineq', 'fun': constraintProbLow3}

c1 = ([conGen1, conGen2, conProb1, conProb2])
cons = ([conGen1, conGen2, conGen3, conProb1, conProb2, conProb3])
bnds = ((0,s),(0,s),(0,s),(0,s),(0,s),(0,s),(0,1),(0,1),(0,1),(0,1))

n=len(bnds)
x0 = np.zeros(n)+0.1

solution = minimize(objective, x0, bounds = bnds, constraints = c1)
print(solution)
np.round(solution.x, decimals = 2)

