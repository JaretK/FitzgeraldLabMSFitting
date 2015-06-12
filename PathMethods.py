'''
Created on Jun 9, 2015

@author: jkarnuta
'''
import datetime

#private function
def _getDirectoryPath(pathIn):
    splitIntoDirs = pathIn.split(r"/")
    del splitIntoDirs[-1]
    return "/".join(splitIntoDirs)+"/"

#returns a file path based on the relative path with a time stamp and _FITTED added
def stampedFileName(pathIn):
    splitIntoDirs = pathIn.split(r"/")
    filename = splitIntoDirs[-1]
    del splitIntoDirs[-1]
    absDirPath =  "/".join(splitIntoDirs)+"/"
    filenamelist =filename.split(".")
    return absDirPath + filenamelist[0]+"_"+str(datetime.date.today())+"_FITTED"+"."+filenamelist[1]

# returns the filepath with the custom name added to the end of the file name
def customFileName(pathIn, customName):
    splitIntoDirs = pathIn.split(r"/")
    filename = splitIntoDirs[-1]
    del splitIntoDirs[-1]
    absDirPath =  "/".join(splitIntoDirs)+"/"
    filenamelist =filename.split(".")
    return absDirPath + filenamelist[0]+customName+"."+filenamelist[1]

#returns the directory where figures should be stored
def figuresFileName(pathIn):
    absPath = _getDirectoryPath(pathIn)
    filename = _getFileName(pathIn)
    return absPath + filename + "_"+str(datetime.date.today())+"_figures"+"/"

#private method to get the file name
def _getFileName(pathIn):
    splitIntoDirs = pathIn.split(r"/")
    return splitIntoDirs[-1].split(".")[0]

#checks to see if file already exists. If it does, add a number to the end of the new file / dir
"""
unfinished, I'll get to it when I get to it
# def _checkExistence(pathIn):
#     import os
#     if os.path.exists(pathIn):
#         
#         if(pathIn.endswith(".csv")):
#             import re
#             match = re.search("(_)")
#             pathIn +="_1.csv"
#             return pathIn
#         
#         elif(pathIn.endswith("/")):
#             del pathIn[-1]
#             pathIn += "_1/"
#             return pathIn
#         
#     return pathIn
"""

if __name__ == "__main__":
    print _getDirectoryPath("/users/jkarnuta/desktop/fitz_lab/r_projects/Matched_Orbitrap_Ariel.csv")
    print stampedFileName("/users/jkarnuta/desktop/fitz_lab/r_projects/Matched_Orbitrap_Ariel.csv")
    print figuresFileName("/users/jkarnuta/desktop/fitz_lab/r_projects/Matched_Orbitrap_Ariel.csv")