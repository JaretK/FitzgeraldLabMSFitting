'''
Created on Jun 8, 2015

@author: jkarnuta
'''
from peptideRun import peptideRun as pepRun
class DataArray:
    def __init__(self, filepath):
        data = []
        fileList = []
        readFile = open (filepath, "rU")
        numLines = 0
        for line in readFile:
            numLines+=1
            fileList.append(line)
        header = (fileList[0],fileList[1], fileList[2])
        del fileList[0]
        del fileList[0]
        
        for item in fileList:
            data.append(pepRun(item, True))
        
        denConcs = []
        primaryHeader = header[1].split(",")
        for i in range(4,12):
            denConcs.append(float(primaryHeader[i]))
            
        self.header = header
        self.denConcs = denConcs
        self.data = data
        self.size = numLines-2

        """
        call information in data via:
        data.sequence
        data.protein
        data.control.intsum, rtmin, denats
        data.ligand.intsum, rtmin, denats
        """
        return
    
    def __str__(self):
        num = 1
        for ele in self.data:
            print "Number = "+str(num)
            print ele
            num+=1
        return ""
            
if __name__ == "__main__":
    data = DataArray("/users/jkarnuta/desktop/fitz_lab/r_projects/Matched_Orbitrap_Ariel.csv")
    print data.data
            
        