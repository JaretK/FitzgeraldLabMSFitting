'''
Created on Jun 8, 2015

@author: jkarnuta
'''
class peptideRun:
    """
    runInfo defined in the following order:
    sequence, protein, int sum, RT (min), denat 1, ..., denat 8, int sum (ligand), RT min, denat 1,...,denat 8
    runinfo is line of csv, containsLigand means contains both control and ligand
    offset is the number of rows offset between the start of the control (on left) and start of the ligand (on right)
    """
    def __init__(self,runInfo, numberDenats ,containsLigand, offset = 10):
        splitChar = ","
        l=[""]
        currentIndex = 0
        withinQuotes = False
        for char in runInfo:
            if char == "\"" and not withinQuotes:
                l[currentIndex]+= char
                withinQuotes = True
            elif char == "\"" and withinQuotes:
                l[currentIndex]+= char
                withinQuotes = False        
            elif char == splitChar and not withinQuotes:
                currentIndex+=1
                l.append("") #make room for the new addition
                continue
            else:
                l[currentIndex]+= char
        controlList = []
        ligandList = []
        
        for i in range(2,4+numberDenats):
            controlList.append(l[i])
            if containsLigand:
                ligandList.append(l[i+offset])

        self.sequence = l[0]
        self.protein = l[1]
        self.control = runData(controlList, numberDenats)
        if containsLigand:
            self.ligand = runData(ligandList, numberDenats)
        else:
            self.ligand = "No Ligand Binding Data Available"
            
    def __str__(self):
        ligandString = self.ligand if isinstance(self.ligand, str) else self.ligand.toString()
        retString = "Sequence: "+self.sequence+"\nProtein: "+self.protein+"\n***Control****\n"+self.control.toString()+"\n***Ligand***\n"+ligandString+"\n"
        return retString
class runData:
    def __init__(self, l, numberDenats):
        self.intsum = float(l[0])
        self.rtmin = float(l[1])
        self.denats = []
        print numberDenats
        for i in range(2,numberDenats+2):
            print l[i]
            self.denats.append(float(l[i]))
        return
    def toString(self):
        intsum = str(self.intsum)
        rtmin = str(self.rtmin)
        denats = str(self.denats)
        return "INTSUM: "+intsum+"\nRT (min): "+rtmin+"\nDENATS: "+denats

if __name__ == "__main__":
    pep = peptideRun("(-)M(OX)LDINQFIEDK(G),\"Seryl-tRNA synthetase, cytoplasmic\",9.21,71.53,1.125884715,0.937793813,1.227384602,0.817350991,0.887553438,0.858088418,1.123378172,0.748661868", False)
    print pep
    
        
        