import codecs
import os

_MainDirectory = "Geografia"
_Files = []
_ActualFile = 0

def getActualFile():
    global _ActualFile
    return _ActualFile
def readDirectories(pPath):
    global _Files
    for file in os.listdir(pPath):
        if file.endswith(".htm"):
            _Files.append(pPath+"/"+str(file))
        elif "." in file :
            return
        else:
            readDirectories(pPath + "/" + str(file))
#Get the next file from the directory specified on readDirectories()
def nextFile():
    global _ActualFile, _Files
    if _ActualFile <= len(_Files)-1:
        file = _Files[_ActualFile]
        _ActualFile += 1
        return file
    else:
        return None
def readFile(pPath): 
    with codecs.open(pPath,'r',encoding='utf8') as file:
        text = file.read()
    return text
def readLines(pPath):
    with open(pPath) as file:
        content = file.readlines()
        return content
#Writes erasing the content 
def writeFile(pPath, pText):
    with codecs.open(pPath,'w',encoding='utf8') as file:
        file.write(pText)
#Writes appending text
def writeFileAppend(pPath, pText):
    with codecs.open(pPath,'a',encoding='utf8') as file:
        file.write(pText)

