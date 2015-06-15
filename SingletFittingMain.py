'''
Created on Jun 9, 2015

@author: jkarnuta
'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as Fit
print __import__("sys").executable
import scipy
print scipy.__file__

"""
For manually fitting small data sets
"""
midpointTolerance = 0.1
#denaturant concentrations
xdataString = "0.5    1      1.7    2    2.5    3    4"
xdata = [float(x) for x in xdataString.split()]
#reporter intensities
ydataString = "1.197490153    1.24113578       1.314496603    1.369742856    0.769925538    0.857576246    0.910579677"
ydata = [float(y) for y in ydataString.split()]

if len(xdata) != len(ydata):
    print "ERROR: vectors not compatible, dimensions not equal"
    raise SystemError

A = max(ydata)
B = min(ydata) 


#Changes the intensities based on the midpointTolerance. To not change intensities, return 
def alterIntensities(intensities):
    return intensities
    newYData = []
    #first pass to change the intensities based on the interval
    for ele in intensities:
        if ele > 1+midpointTolerance:
            ele = 1
        elif (ele >= 1- midpointTolerance) and (ele <= 1+midpointTolerance):
            ele = 0.5
        elif (ele < 1-midpointTolerance):
            ele = 0
        newYData.append(ele)
    #second pass to clean up intensities by checking neighbors
    for i in range(len(newYData)):
        prev = 0
        current = newYData[i]
        next_val = 0
        if i == 0:
            prev = current
        elif i == len(newYData)-1:
            next_val = current
        if (prev == next_val):
            current = prev
    return newYData

ydata = alterIntensities(ydata)

def makeModel(x, dGf, m):
    kox = 0.013 #1/s
    t = 180 #s
    RT = 0.592154 #kcal/mol
    Kfold = 1+np.exp(-(dGf + np.multiply(m, x))/RT)
    return B+(A-B)*np.exp(-(kox*t)/Kfold)

def makeChalfModel(x, chalf, b, A, B):
    #b = 0.592154/float(m_val)
    return A + (B-A)/(1+np.exp(-(x-chalf)/(b)))

try:
    try:
        popt, pcov = Fit(makeModel, xdata, ydata)
        if not isinstance(pcov, np.ndarray):
            raise RuntimeError
    except RuntimeError:
        popt, pcov = Fit(makeModel, xdata, ydata,0)
except RuntimeError:
    print "Max recursion depth exceeded on dGf, m"
if not isinstance(pcov, np.ndarray):
    print "Covariance matrix is INF on dGf, m"
    print ""

perr = np.sqrt(np.diag(pcov))
dGf_val = str(popt[0])
m_val = str(popt[1])
dGf_err = str(perr[0])
m_err = str(perr[1])

try:
    ch, ch_cov = Fit(makeChalfModel, xdata, ydata)
except RuntimeError:
    print "Max recursion depth exceeded on c_half"
if not isinstance(ch_cov, np.ndarray):
    print "Covariance matrix is INF on c_half"
 
chalf_val = str(ch[0])
chalf_err = str(np.sqrt(np.diag(ch_cov))[0])
b_val = str(ch[1])
b_err = str(np.sqrt(np.diag(ch_cov))[1])


print "dGf: "+dGf_val+" +/- "+dGf_err
print "  m: "+m_val+" +/- "+m_err
print "C12: "+chalf_val +"+/-"+chalf_err
print "  b: "+b_val+"+/-"+b_err

plottedXData = np.linspace(xdata[0], xdata[-1], num = 100) 
ylim =[min(ydata)*0.9, max(ydata)*1.1]
fittedModel = makeModel(plottedXData, float(dGf_val), float(m_val))
chalfModel= makeChalfModel(plottedXData, float(chalf_val), float(b_val))
plt.figure()
plt.scatter(xdata, ydata, label = "Data", marker = 'o', alpha = 0.5)
plt.plot(plottedXData, fittedModel ,"r",label = "dGf, m model")
plt.plot(plottedXData, chalfModel, "g", label = "C 1/2, b Model")
plt.legend()
plt.ylim(ylim)
plt.show()