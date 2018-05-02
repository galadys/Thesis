# -*- coding: utf-8 -*-

from GivenProb import CDF, PDF
import numpy as np
import matplotlib.pyplot as plt

lambdaB = 3 #Buyer's exponential distribution parameter
lambdaS = 3 #Seller's exponential distribution parameter
dist = 4
s = 9
numB = 1000
numS = 600
numH = 1500
numL = 2000
r = .1
ph = 5
pl = 3
x1 = .5
l1 = 1

X = np.linspace(0, 5,100, endpoint=True)

numL = CDF((ph - X)/x1, lambdaB) - CDF((s-X)/(1+x1), lambdaB)
pL = r*numL - r*X*(PDF((ph - X)/x1, lambdaB)-PDF((s-X)/(1+x1), lambdaB)) + r*ph*PDF((ph - X)/x1, lambdaB)

ypLmax = max(pL)
xpLmax = X[pL.argmax(axis=0)]
fig = plt.figure()
plt.plot(X, pL)
fig.suptitle('Comparative Statics: Changes in Price')
plt.xlabel('Price of Low-Quality Ride')
plt.ylabel('Derivative of Firm\'s Profit')
#plt.savefig('test.jpg')

numH = 1-CDF((X-pl)/x1, lambdaB)
pH = r*numH-r*X*(PDF((X-pl)/x1, lambdaB))+ r*pl*(PDF((X-pl)/x1, lambdaB))

fig = plt.figure()
plt.plot(X, pH)
fig.suptitle('Comparative Statics: Changes in Price, with low-price=3')
plt.xlabel('Price of High-Quality Ride')
plt.ylabel('Derivative of Firm\'s Profit')
#plt.savefig('test.jpg')

X2 = np.linspace(0.01, 1,100, endpoint=False)

prob1= r*pl*(-PDF((ph-pl)/X2,lambdaB)*(ph-pl)/pow(X2,2)+PDF((s-pl)/(1+X2), lambdaB)*(s-pl)/pow(1+X2,2))+r*ph*(PDF((ph-pl)/X2, lambdaB)*(ph-pl)/pow(X2,2))
fig = plt.figure()
plt.plot(X2, prob1)
fig.suptitle('Comparative Statics: Changes in Pooling Probability')
plt.xlabel('Pooling Probability')
plt.ylabel('Derivative of Firm\'s Profit')



X = np.linspace(0, 5,100, endpoint=True)

x1=.5
numL = CDF((ph - X)/x1, lambdaB) - CDF((s-X)/(1+x1), lambdaB)
G1 = CDF((numH*(ph-r)+ numL*(X-r))/(numH + (1+x1)*numL), lambdaS)- CDF((ph-X)/x1, lambdaB) + (1-x1)*CDF((ph - X)/x1, lambdaB) - CDF((s-X)/(1+x1), lambdaB)
dG1 = np.zeros(G1.shape, np.float)
dG1[0:-1] = np.diff(G1)/np.diff(X)
dG1[-1] = (G1[-1] - G1[-2])/(X[-1] - X[-2])
pL2 = r*numL - r*X*(PDF((ph - X)/x1, lambdaB)-PDF((s-X)/(1+x1), lambdaB)) + r*ph*PDF((ph - X)/x1, lambdaB) -l1*(dG1)

fig = plt.figure()
plt.plot(X, pL2)
fig.suptitle('Comparative Statics: Changes in Price')
plt.xlabel('Price of Low-Quality Ride')
plt.ylabel('Derivative of Firm\'s Profit')