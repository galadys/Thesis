import numpy as np 
from scipy.optimize import minimize
from temp import NH1, NL1
from scipy.stats import  expon

lambdaB = 1 #Buyer's exponential distribution parameter
lambdaS = 1 #Seller's exponential distribution parameter
dist = 1
s = 4


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
    return 1- CDF((NH(x, location)*(x[3+location]-x[6+location])+NL(x, location)*(x[location]-x[6+location]))/(NH(x, location) + (1-x[7+ location])*NL(x, location)+2*x[7+location]*NL(x, location)), lambdaS)

def constraintGenEq(x, location):
    return NS(x, location)- NH(x, location) -(1+x[7+location])*NL(x, location)

conGen1= {'type': 'eq', 'fun': constraintGenEq(x, 0)} #this wont work
conGen2= {'type': 'eq', 'fun': constraintGenEq(x, 1)}
conGen3= {'type': 'eq', 'fun': constraintGenEq(x, 2)}


