import numpy as np 
from scipy.optimize import minimize
from scipy.stats import  expon

lambdaB = 1 #Buyer's exponential distribution parameter
lambdaS = 1 #Seller's exponential distribution parameter
dist = 4
s = 9


def CDF(x, parameter):
    return expon.cdf(x, scale = 1/parameter)

def PDF(x, parameter):
    return expon.pdf(x, scale = 1/parameter)

prob = [0.5, 0.5, 0.5]

def objective(x):
    r = x[6] =.1
    PL = [x[0], x[1], x[2]]
    PH = [x[3], x[4], x[5]]
    location = [0,1,2]
    output = 0
    for i in location:
        output = output + r*(NL(x, i, prob)*PL[i] + NH(x, i, prob)*PH[i])
    return -output

def NH(x, location, prob):
    return 1-CDF((x[3+location]-x[0+location])/(prob[location]), lambdaB)
        
def NL(x, location, prob):
    return CDF((x[3+location]-x[0+location])/prob[location], lambdaB) - CDF((s-x[0+location])/(1+prob[location]), lambdaB)

def NS(x, location, prob):
    return 1- CDF(
            (NH(x, location, prob)*(x[3+location]-x[6])+NL(x, location, prob)*(x[location]-x[6]))
            /(NH(x, location, prob) + (1-prob[location])*NL(x, location, prob)+2*prob[location]*NL(x, location, prob))
            , lambdaS)

def constraintGenEq1(x, location = 0):
    return NS(x, location, prob)- NH(x, location, prob) -(1+prob[location])*NL(x, location, prob)
def constraintGenEq2(x, location = 1):
    return NS(x, location, prob)- NH(x, location, prob) -(1+prob[location])*NL(x, location, prob)
def constraintGenEq3(x, location = 2):
    return NS(x, location, prob)- NH(x, location, prob) -(1+prob[location])*NL(x, location, prob)

def constraintProbLow1(x):
    return x[7] - (x[3]-x[0])/(dist) 
def constraintProbLow2(x):
    return x[8] - (x[4]-x[1])/(dist) 
def constraintProbLow3(x):
    return x[9] - (x[5]-x[2])/(dist) 

conGen1= {'type': 'ineq', 'fun': constraintGenEq1} 
conGen2= {'type': 'ineq', 'fun': constraintGenEq2}
conGen3= {'type': 'ineq', 'fun': constraintGenEq2}
conProb1= {'type': 'ineq', 'fun': constraintProbLow1}
conProb2= {'type': 'ineq', 'fun': constraintProbLow2}
conProb3= {'type': 'ineq', 'fun': constraintProbLow3}

c1 = ([conGen1, conGen2, conGen3])
cons = ([conGen1, conGen2, conGen3, conProb1, conProb2, conProb3])
bnds1 = ((0,s),(0,s),(0,s),(0,s-dist),(0,s-dist),(0,s-dist),(0,1))
bnds2 = ((0,s),(0,s),(0,s),(0,s),(0,s),(0,s),(0,1),(0,1),(0,1),(0,1))

n=len(bnds1)
x0 = np.zeros(n)+0.1

solution = minimize(objective, x0, bounds = bnds1, constraints = c1)
print(solution)
np.round(solution.x, decimals = 2)

parameterList = []

def altminimize(objective, x0, bounds=bnds1, constraints=c1):
    global parameterList
    solution = minimize(objective, x0, bounds=bounds, constraints=constraints)
    parameterList.append( (x0, bounds, constraints, solution.x) )
    return print(solution)

altminimize(objective, x0, bnds1, c1)
parameterList
