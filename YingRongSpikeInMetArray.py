'''
Created on Jun 9, 2015

@author: jkarnuta
'''
'''
Created on Jun 8, 2015

@author: jkarnuta
'''
from peptideRun import peptideRun as pepRun
class DataArray:
    def __init__(self, filepath, numberDenats):
        data = []
        fileList = []
        readFile = open (filepath, "rU")
        numLines = 0
        for line in readFile:
            numLines+=1
            fileList.append(line)
            
        header = [fileList[0]]
        try:
            if not self.__correctFormat(header):
                raise TypeError("This file format is not supported. Please see sample file format\n")
        except TypeError:
            raise SystemExit("Exiting due to incorrect format")
        
        del fileList[0]
        
        for item in fileList:
            data.append(pepRun(item, numberDenats ,False))
        
            
        self.header = header
        self.data = data
        self.size = numLines-len(header)

        """
        call information in data via:
        data.sequence
        data.protein
        data.control.intsum, rtmin, denats
        data.ligand.intsum, rtmin, denats
        """
        return
    
    def setDenConcs(self, custom):
        self.denConcs = [float(x) for x in custom]
        return 
    
    def __str__(self):
        num = 1
        for ele in self.data:
            print "Number = "+str(num)
            print ele
            num+=1
        return ""
    
    def __correctFormat(self, header):
        if not "sequence" in header[0]:
            return False
        return True
            
if __name__ == "__main__":
    data = DataArray("/users/jkarnuta/desktop/AverageMultipleSpikeinMet.csv")
    print data.data[1]
            
        