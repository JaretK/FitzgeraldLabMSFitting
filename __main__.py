'''
Created on Jun 8, 2015
 
@author: jkarnuta
'''
import os 
import numpy as np
from scipy.optimize import curve_fit
import re
from csvReader import csvReader
import matplotlib.pyplot as plt
from FileWriter import FileWriter
from PathMethods import figuresFileName
import sys

vi = sys.version_info
if vi[0] != 2 or vi[1] != 6:
    print "ERROR: python interpreter of wrong version. Requires 2.6.x"
    raise SystemExit
print sys.argv
##-------------------------------------------
from YingRongSpikeInMetArray import DataArray
filepath = sys.argv[1]
denatsFile = sys.argv[2]
pictureFolder = figuresFileName(filepath)
fw = FileWriter(filepath, customFileName="")

#If a third argument is passed, generate figures
#Figure generation is slow, so it is often optimal to disregard generation
#as fitting is <5 second operation 
runFigs = False
try:
    sys.argv[3]
    runFigs = True
    #Check if pictureFolder exists, if not mkdir
    if not os.path.exists(pictureFolder):
        os.makedirs(pictureFolder)
except IndexError:
    pass
##-------------------------------------------

denaturantsArray = csvReader(denatsFile).getHeader()
#Populate data array with data from csv input file
data = DataArray(filepath, len(denaturantsArray))

#Set up denaturant concentrations from denatsFile (sys.argv[2]
data.setDenConcs(denaturantsArray)
xdata = np.array(data.denConcs)
    
#Changes the intensities based on the midpointTolerance. To not change intensities, return 
def alterIntensities(intensities):
    return intensities


#Make custom header (if there is a new line, remove)
newHeader = data.header
newHeader[-1] = re.sub(r"\n", "",newHeader[-1])
newHeader.append("A")
newHeader.append("B")
newHeader.append("dGf")
newHeader.append("sd dGf")
newHeader.append("m")
newHeader.append("sd m")
newHeader.append("C 1/2")
newHeader.append("sd C 1/2")
newHeader.append("b")
newHeader.append("sd b")
newHeader[-1] = newHeader[-1]+"\n"
#Write header to file
fw.writeList(data.header)

def makeModel(x, dGf, m):
    kox = 0.013 #1/s
    t = 180 #s
    RT = 0.592154 #kcal/mol
    Kfold = 1+np.exp(-(dGf + np.multiply(m, x))/RT)
    return B+(A-B)*np.exp(-(kox*t)/Kfold)

def makeChalfModel(x, chalf, b):
    return A + (B-A)/(1+np.exp(-(x-chalf)/(b)))

allattempts = []
failedOnRuntime = []
failedOnCovMatrix = []
numSuccess = 0
numRuntimeError_dGf_m = 0
numCovINF_dGf_m = 0
numRuntimeError_chalf_b = 0
numCovINF_chalf_b = 0
i=0
for i in range(data.size):
    ##-----------------------------------
    ydata = np.array(data.data[i].control.denats)
    ##-----------------------------------    
    sequence = data.data[i].sequence
    protein = data.data[i].protein
    score = str(data.data[i].control.intsum)
    rtmin = str(data.data[i].control.rtmin)
    #A = ydata[0]
    #B = ydata[len(ydata)-1]
    A = max(ydata)
    B = min(ydata)  
    ydata = alterIntensities(ydata)
    
    message = [sequence, protein, score, rtmin]
    for ele in ydata:
        message.append(str(ele))
    message.append(str(A))
    message.append(str(B))
    
    try:
        #use either 3 or 4 parameter curve_fit
        try:
            popt, pcov = curve_fit(makeModel, xdata, ydata)
            if not isinstance(pcov, np.ndarray):
                raise RuntimeError
        except RuntimeError:
            popt, pcov = curve_fit(makeModel, xdata, ydata,0)
    except RuntimeError:
        print "Max recursion depth exceeded on dGf, m"
        print "Could not find fit for RUN: "+str(i+1)
        print "Sequence: "+sequence
        print "Protein: "+protein
        print data.data[i].control.toString()
        print ""
        numRuntimeError_dGf_m +=1
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        
        failedOnRuntime.append(str(i+2))
        allattempts.append(message)
        message[-1] = message[-1]+"\n"
        fw.writeList(message)
        continue
    
    if not isinstance(pcov, np.ndarray):
        print "Covariance matrix is INF on dGf, m"
        print "Could not find fit for RUN: "+str(i+1)
        print "Sequence: "+sequence
        print "Protein: "+protein
        print data.data[i].control.toString()
        print ""
        numCovINF_dGf_m +=1
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        
        failedOnCovMatrix.append(str(i+2))
        allattempts.append(message)
        message[-1] = message[-1]+"\n"
        fw.writeList(message)
        continue
     
    perr = np.sqrt(np.diag(pcov))
    dGf_val = str(popt[0])
    m_val = str(popt[1])
    dGf_err = str(perr[0])
    m_err = str(perr[1])
    message.append(dGf_val)
    message.append(dGf_err)
    message.append(m_val)
    message.append(m_err)
    
    try:
        try:
            ch, ch_cov = curve_fit(makeChalfModel, xdata, ydata)
            if not isinstance(pcov, np.ndarray):
                raise RuntimeError
        except RuntimeError:
            ch, ch_cov = curve_fit(makeChalfModel, xdata, ydata, p0=[1,0.592154/float(m_val)])
    except RuntimeError:
        print "Max recursion depth exceeded on C 1/2"
        print "Could not find fit for RUN: "+str(i+1)
        print "Sequence: "+sequence
        print "Protein: "+protein
        print data.data[i].control.toString()
        print ""
        numRuntimeError_chalf_b +=1
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        failedOnRuntime.append(
                               str(i+2))
        allattempts.append(message)
        message[-1] = message[-1]+"\n"
        fw.writeList(message)
        continue
    
    if not isinstance(ch_cov, np.ndarray):
        print "Covariance matrix is INF on C 1/2"
        print "Could not find fit for RUN: "+str(i+1)
        print "Sequence: "+sequence
        print "Protein: "+protein
        print data.data[i].control.toString()
        print ""
        numCovINF_chalf_b +=1
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        message.append("NaN")
        
        failedOnCovMatrix.append(str(i+2))
        allattempts.append(message)
        message[-1] = message[-1]+"\n"
        fw.writeList(message)
        continue
    
    chalf_val = str(ch[0])
    chalf_err = str(np.sqrt(np.diag(ch_cov))[0])
    b_val = str(ch[1])
    b_err = str(np.sqrt(np.diag(ch_cov))[1])
    message.append(chalf_val)
    message.append(chalf_err)
    message.append(b_val)
    message.append(b_err)
    
    message[-1] = message[-1]+"\n"
    allattempts.append(message)
    fw.writeList(message)
    
    print "Run #"+str(i+1)
    print "dGf: "+dGf_val+" +/- "+dGf_err
    print "  m: "+m_val+" +/- "+m_err
    print "C12: "+chalf_val+"+/-"+chalf_err
    print "  b: "+b_val+"+/-"+b_err
    print ""
    numSuccess += 1
    
fw.close()
if runFigs:
    for i in range(data.size):
        numberToView = i+2
        if numberToView == -1:
            raise SystemExit
        print "Drawing Fig"+str(numberToView)+".png"
        plottedYData = [float(x) for x in allattempts[numberToView - 2][4:12]]
        A = float(allattempts[numberToView-2][12])
        B = float(allattempts[numberToView-2][13])
        m_val = float(allattempts[numberToView-2][16])
        plottedXData = np.linspace(xdata[0], xdata[-1], num = 100) 
        params = (float(allattempts[numberToView-2][14]), m_val)
        chalf_val = float(allattempts[numberToView-2][18])
             
        ylim =[min(plottedYData)*0.9, max(plottedYData)*1.1]
        fittedModel = makeModel(plottedXData,*params)
        chalfModel= makeChalfModel(plottedXData, float(chalf_val), float(b_val))
             
        plt.figure()
        plt.title(allattempts[numberToView-2][0])
        plt.scatter(xdata, plottedYData, label = "Data", marker = 'o', alpha = 0.5)
        plt.plot(plottedXData, fittedModel ,"r",label = "fitted model")
        plt.plot(plottedXData, chalfModel, "g", label = "C 1/2 Model")
        plt.legend()
        plt.ylim(ylim)
        plt.savefig(pictureFolder +"Fig"+str(numberToView)+".png",bbox_inches='tight')
    
    print "finished rasterizing images"
else:
    "Figures not being generated for this run."
    
print ""
print "Run Statistics: "
print "Number Successful: "+str(numSuccess) + " ("+str((float(numSuccess)/data.size)*100)+"%)"
print "Number Failed at Runtime on dGf, m: "+str(numRuntimeError_dGf_m)
print "Number with INF Covariance Matrix on dGf, m: "+str(numCovINF_dGf_m)
print "Number Failed at Runtime on chalf, b: "+str(numRuntimeError_chalf_b)
print "Number with INF Covariance Matrix on chalf, b: "+str(numCovINF_chalf_b)
print ""
print "Failed on runtime: "+str(failedOnRuntime)
print ""
print "Failed on Cov Matrix: "+str(failedOnCovMatrix)
