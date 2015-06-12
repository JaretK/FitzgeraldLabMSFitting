'''
Created on Jun 12, 2015

@author: jkarnuta
'''

class csvReader:
    def __init__(self, filepath):
        self.file = open(filepath, "rU")
        self.bins = []
        for line in self.file:
            self.bins.append([x.strip() for x in line.split(",")])
        self.file.close()
        
    def getHeader(self):
        return self.bins[0]    
    
    def getAllBins(self):
        return self.bins
        
if __name__ == "__main__":
    fr = csvReader("/users/jkarnuta/desktop/eightTags.csv")
    print fr.getHeader()