from libs import FileHandler
from libs import TextAnalizer
from math import log10
import copy
import collections
import gc
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
    dictionaryText = ""
    for iTerm in range(len(_TermsFrequences)):
        for iDocument in range(len(_DocumentsPaths)):
            lenght +=_TermsFrequences[iTerm][1][iDocument]
        dictionaryText += _TermsFrequences[iTerm][0]+"\t"+str(init)+"\t"+ str(lenght)+"\n"
        init += lenght
        lenght = 0
    FileHandler.writeFile("Diccionario.txt",dictionaryText)
    print("Dictionary file created")
    
def createPostingsFile():
    global _TermsWeights,_DocumentPaths,_TermsFrequences
    FileHandler.writeFile("Postings.txt","")
    postingsText = ""
    for iDocument in range(len(_DocumentsPaths)):
        for iTerm in range (len(_TermsFrequences)):
            if _TermsFrequences[iTerm][1][iDocument] != 0:
                postingsText += str(iDocument)+"\t"+str(_TermsWeights[iTerm][1][iDocument])+"\n"
    FileHandler.writeFile("Postings.txt",postingsText)
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
    return idf
def calculateWeights(pIDF):
    global _TermsWeights,_TermsFrequences
    _TermsWeights = copy.deepcopy(_TermsFrequences)
    for iDocument in range(len(_DocumentsPaths)):
        for iTerm in range(len( _TermsFrequences)):
            _TermsWeights[iTerm][1][iDocument] = log10(1+_TermsWeights[iTerm][1][iDocument])*pIDF[iTerm]
    
        

#------------------Main-----------------#
createDocumentsFile()
_DocumentsPaths = _DocumentsPaths[0:10]
_TermsFrequences = TextAnalizer.analizeDocuments(_DocumentsPaths)
_TermsFrequences = createSortedList(_TermsFrequences)
idf = calculateIDF()
calculateWeights(idf)
createDictionaryFile()
gc.collect()
createPostingsFile()

