from libs import FileHandler
from libs import TextAnalizer
from math import log10
import copy
import collections
_TermsFrequences = {}
_DocumentsPaths = []
_TermsWeights = {}
def createDocumentsFile():
    global _DocumentsPaths
    FileHandler.readDirectories("Geografia")
    FileHandler.writeFile("Documentos.txt","")
    path = FileHandler.nextFile()
    while path != None:
        FileHandler.writeFileAppend("Documentos.txt",str(FileHandler.getActualFile())+"\t\t"+path+"\n")
        _DocumentsPaths.append(path)
        path = FileHandler.nextFile()
    print("Documents file created")
def dictionaryToList(pDictionary):
    sortedList = []
    for key, value in sorted(pDictionary.items()):
        sortedList.append([key,value])
    return sortedList
def createSortedList(pDictionary): 
    sortedCollection = dictionaryToList(pDictionary)
    #sortedCollection = sortedCollection[1:]
    while True:
        if sortedCollection[-1][0][0]=="ñ":
            sortedCollection = moveLast(sortedCollection)
        else:
            break
    return sortedCollection

def createDictionaryFile():
    global _TermsFrequences,_DocumentPaths
    lenght = 0
    FileHandler.writeFile("Diccionario.txt","")
    init = 0

    for iTerm in range(len(_TermsFrequences)):
        for iDocument in range(len(_DocumentsPaths)):
            lenght +=_TermsFrequences[iTerm][1][iDocument]
        #FileHandler.writeFileAppend("Diccionario.txt",key+"\t"+str(init)+"\t"+ str(lenght)+"\n")
        FileHandler.writeFileAppend("Diccionario.txt",_TermsFrequences[iTerm][0]+"\t"+str(init)+"\t"+ str(lenght)+"\n")
        init += lenght
        lenght = 0
    
##    for key, value in _TermsFrequences.items():
##        for iDocument in range(len(_DocumentsPaths)):
##            lenght +=_TermsFrequences[key][iDocument]
##        FileHandler.writeFileAppend("Diccionario.txt",key+"\t"+str(init)+"\t"+ str(lenght)+"\n")
##        init += lenght
##        lenght = 0
    print("Dictionary file created")
    
def createPostingsFile():
    global _TermsWeights,_DocumentPaths,_TermsFrequences
    #iTerm = 0
    FileHandler.writeFile("Postings.txt","")
    
    for iDocument in range(len(_DocumentsPaths)):
        for iTerm in range (len(_TermsFrequences)):
            if _TermsFrequences[iTerm][1][iDocument] != 0:
                FileHandler.writeFileAppend("Postings.txt",str(iDocument)+"\t"+str(_TermsWeights[iTerm][1][iDocument])+"\n")

            
##    for iDocument in range(len(_DocumentsPaths)):
##        for key, value in _TermsFrequences.items():
##            if value[iDocument] != 0:
##                FileHandler.writeFileAppend("Postings.txt",str(iDocument)+"\t"+str(value[iDocument])+"\n")
##            iTerm += 1
##        iTerm = 0
    print("Postings file created")
    
def calculateIDF():
    global _TermsFrequences,_DocumentsPaths
    N = len(_DocumentsPaths)
    Ni = [0]*len(_TermsFrequences)
    idf = [0]*len(_TermsFrequences)
    for iDocument in range(len(_DocumentsPaths)):
        for iTerm in range(len(_TermsFrequences)):
            if _TermsFrequences[iTerm][1][iDocument] != 0:
                Ni[iTerm] += 1
    for iTerm in range(len(Ni)):
        if Ni[iTerm] != 0:
            idf[iTerm] = log10(N/Ni[iTerm])
    
    
##    for iDocument in range(len(_DocumentsPaths)):
##        for key, value in _TermsFrequences.items():
##            if value[iDocument] != 0:
##                Ni[iTerm] += 1
##            iTerm += 1
##        iTerm = 0
##    for iTerm in range(len(Ni)):
##        if Ni[iTerm] != 0:
##            idf[iTerm] = log10(N/Ni[iTerm])
    return idf
def calculateWeights(pIDF):
    global _TermsWeights,_TermsFrequences
    _TermsWeights = copy.deepcopy(_TermsFrequences)
    print(_TermsWeights)
    for iDocument in range(len(_DocumentsPaths)):
        for iTerm in range(len( _TermsFrequences)):
            _TermsWeights[iTerm][1][iDocument] = log10(1+_TermsWeights[iTerm][1][iDocument])*pIDF[iTerm]
    
##    for iDocument in range(len(_DocumentsPaths)):
##        for key, value in _TermsWeights.items():
##            _TermsWeights[key][iDocument] = log10(1+value[iDocument])*pIDF[iTerm]
##            iTerm += 1
##        iTerm = 0
        

#------------------Main-----------------#
createDocumentsFile()
_DocumentsPaths = _DocumentsPaths[0:5]
_TermsFrequences = TextAnalizer.analizeDocuments(_DocumentsPaths)
_TermsFrequences = createSortedList(_TermsFrequences)
idf = calculateIDF()
calculateWeights(idf)
createDictionaryFile()
createPostingsFile()

