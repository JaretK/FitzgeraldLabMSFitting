'''
Created on Jun 9, 2015

@author: jkarnuta
'''
import PathMethods

#wrapper to mimic the filewriter class in java
class FileWriter:
    def __init__(self, filepath, customFileName = ""):
        if customFileName == "":
            self.writer = open(PathMethods.stampedFileName(filepath), "w")
        else:
            self.writer = open(PathMethods.customFileName(filepath, customFileName), "w")
        
    def writeString(self, stringToWrite):
        self.writer.write(stringToWrite)
    
    def writeList(self, listToWrite):
        self.writeString(",".join(listToWrite))
    
    def close(self):
        self.writer.flush()
        self.writer.close()
        del self
        

if __name__ == "__main__":
    fw = FileWriter("/users/jkarnuta/desktop/touchedFile.csv")
    fw.close()