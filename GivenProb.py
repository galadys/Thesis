import numpy as np 
from scipy.optimize import minimize
from scipy.stats import  expon

lambdaB = 3 #Buyer's exponential distribution parameter
lambdaS = 3 #Seller's exponential distribution parameter
dist = 4
s = 9
numB = 1000
numS = 600


def CDF(x, parameter):
    return expon.cdf(x, scale = 1/parameter)

def PDF(x, parameter):
    return expon.pdf(x, scale = 1/parameter)

def objective(x):
    r = x[6] #=.1
    PL = [x[0], x[1], x[2]]
    PH = [x[3], x[4], x[5]]
    #prob = [x[7], x[8], x[9]]
    location = [0,1,2]
    output = 0
    for i in location:
        output = output + r*(NL(x, i)*PL[i] + NH(x, i)*PH[i])
    return -output

def NH(x, location):
    return 1-CDF((x[3+location]-x[location])/(x[7+location]), lambdaB)
        
def NL(x, location):
    return max(CDF((x[3+location]-x[location])/x[7+location], lambdaB) - CDF((s-x[location])/(1+x[7+location]), lambdaB), 0)

def NS(x, location):
    return  CDF(
            ((NH(x, location)*x[3+location])*(1-x[6])+(NL(x, location)*x[location])*(1-x[6]))
            /(NH(x, location) + (1-x[7+location])*NL(x, location)+2*x[7+location]*NL(x, location))
            , lambdaS)

def constraintGenEq1(x, location = 0):
    return numS*NS(x, location)- numB*NH(x, location) -numB*(1-x[8]/2-x[9]/2)*NL(x, location)
def constraintGenEq2(x, location = 1):
    return numS*NS(x, location)- numB*NH(x, location) -numB*(1-x[7]/2-x[9]/2)*NL(x, location)
def constraintGenEq3(x,location = 2):
    return numS*NS(x, location)- numB*NH(x, location) -numB*(1-x[7]/2-x[8]/2)*NL(x, location)


conGen1= {'type': 'eq', 'fun': constraintGenEq1} 
conGen2= {'type': 'eq', 'fun': constraintGenEq2}
conGen3= {'type': 'eq', 'fun': constraintGenEq3}



cons = ([conGen1, conGen2, conGen3])
bnds1 = ((0,s-dist),(0,s-dist),(0,s-dist),(0,s-dist),(0,s-dist),(0,s-dist),(0,1),(0,1),(0,1),(0,1))

n=len(bnds1)
x0 = np.zeros(n)+0.1

solution = minimize(objective, x0, bounds = bnds1, constraints = cons, options = {'maxiter': 100})
print(solution)
np.round(solution.x, decimals = 2)

parameterList = []#{'service':, 'distance':, 'initial':, 'bounds':, 'constraints':, 'solution':}

def altminimize(objective, x0, bounds=bnds1, constraints=cons):
    global parameterList, s, dist, prob
    solution = minimize(objective, x0, bounds=bounds, constraints=constraints)
    parameterList.append( dict(probs= prob,service=s, distance= dist,initial =x0, bounds=bounds, constraints=constraints, solution=solution.x) )
    return print(solution)

altminimize(objective, x0, bnds1, cons)
parameterList

prob1 = (solution.x[3]-solution.x[0])/dist
prob = [prob1, prob1, prob1]

