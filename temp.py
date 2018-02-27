# -*- coding: utf-8 -*-

import numpy as np 
from scipy.optimize import minimize
from scipy.stats import  expon

lambdaB = 1 #Buyer's exponential distribution parameter
lambdaS = 1 #Seller's exponential distribution parameter
dist = 1
s = 4


def CDF(x, parameter):
    return expon.cdf(x, scale = 1/parameter)

def PDF(x, parameter):
    return expon.pdf(x, scale = 1/parameter)

def objective1(x): #x <-> pl1 pl2 pl3 ph1 ph2 ph3 r prob1 prob2 prob3
    return -x[6]*(x[0]*NL1(x)+x[1]*NL2(x)+x[2]*NL3(x)+x[3]*NH1(x)+x[4]*NH2(x)+x[5]*NH3(x))

def NH1(x): #Number of high buyers at location 1
    return 1-CDF((x[3]-x[0])/(x[7]), lambdaB)
def NH2(x):
    return 1-CDF((x[4]-x[1])/(x[8]), lambdaB)
def NH3(x):
    return 1-CDF((x[5]-x[2])/(x[9]), lambdaB)

def NL1(x): #Number of low buyers at location 1
    return CDF((x[3]-x[0])/x[7], lambdaB) - CDF((s-x[0])/(1+x[7]), lambdaB)
def NL2(x):
    return CDF((x[4]-x[1])/x[8], lambdaB) - CDF((s-x[1])/(1+x[8]), lambdaB)
def NL3(x):
    return CDF((x[5]-x[2])/x[9], lambdaB) - CDF((s-x[2])/(1+x[9]), lambdaB)

def NS1(x): #Number of sellers at location 1
    return 1- CDF((NH1(x)*(x[3]-x[6])+NL1(x)*(x[0]-x[6]))/(NH1(x) + (1-x[7])*NL1(x)+2*x[7]*NL1(x)), lambdaS)
def NS2(x):
    return 1- CDF((NH2(x)*(x[4]-x[6])+NL2(x)*(x[1]-x[6]))/(NH2(x) + (1-x[8])*NL2(x)+2*x[8]*NL2(x)), lambdaS)
def NS3(x):
    return 1- CDF((NH3(x)*(x[5]-x[6])+NL3(x)*(x[2]-x[6]))/(NH3(x) + (1-x[9])*NL3(x)+2*x[9]*NL3(x)), lambdaS)

def constraintGenEq1(x):
    return NS1(x)- NH1(x) -(1+x[7])*NL1(x)
def constraintGenEq2(x):
    return NS2(x)- NH2(x) -(1+x[8])*NL2(x)
def constraintGenEq3(x):
    return NS3(x)- NH3(x) -(1+x[9])*NL3(x)
  
def constraintProbLow1(x):
    x[7] =  (x[3]-x[0])/(dist) 
    return x[7] - (x[3]-x[0])/(dist) 
def constraintProbLow2(x):
    x[8] =  (x[4]-x[1])/(dist) 
    return x[8] - (x[4]-x[1])/(dist) 
def constraintProbLow3(x):
    x[9] =  (x[5]-x[2])/(dist) 
    return x[9] - (x[5]-x[2])/(dist) 

def constraint1(x):
    return NL1(x)
def constraint2(x):
    return NL2(x)
def constraint3(x):
    return NL3(x)

conGen1= {'type': 'eq', 'fun': constraintGenEq1}
conGen2= {'type': 'eq', 'fun': constraintGenEq2}
conGen3= {'type': 'eq', 'fun': constraintGenEq3}
conProb1= {'type': 'ineq', 'fun': constraintProbLow1}
conProb2= {'type': 'ineq', 'fun': constraintProbLow2}
conProb3= {'type': 'ineq', 'fun': constraintProbLow3}
con1 = {'type': 'ineq', 'fun': constraint1}
con2 = {'type': 'ineq', 'fun': constraint2}
con3 = {'type': 'ineq', 'fun': constraint3}

upper = 150
cons = ([conGen1, conGen2, conGen3, conProb1, conProb2, conProb3, con1, con2, con3])
bnds = ((0,upper),(0,upper),(0,upper),(0,upper),(0,upper),(0,upper),(0,1),(0,1),(0,1),(0,1))

n=len(bnds)
x0 = np.zeros(n)+0.1

solution = minimize(objective1,x0, bounds = bnds, constraints = cons)






# -*- coding: utf-8 -*-

