from libs import FileHandler
from nltk import PorterStemmer
from nltk import word_tokenize
from nltk.stem import SnowballStemmer
import re 

_TermsFrequences = {}
_DocumentsPaths = []

def analizeDocuments(pDocumentsPaths):
    global _TermsFrequences,_DocumentsPaths
    _DocumentsPaths = pDocumentsPaths
    for iDocument in range(len(_DocumentsPaths)):
        documentPath = _DocumentsPaths[iDocument]
        text = FileHandler.readFile(documentPath)
        text = removeTags(text)
        text = removeStopWords(text)
        stemmed_words = steamS(text)
        addWords(stemmed_words, _TermsFrequences,iDocument)
        print("Document "+ str(iDocument) + " analized")
    return _TermsFrequences
        
def addWords(pWords,pDictionary,pDocumentID): 
    for iWord in(pWords):
        if iWord in pDictionary:
            pDictionary[iWord][pDocumentID] = pDictionary[iWord][pDocumentID]+1
        else:
            pDictionary[iWord]=[0]*len(_DocumentsPaths)
            pDictionary[iWord][pDocumentID]=1
def getStopWords():
    stopWordFile = FileHandler.readFile("stopwords.txt").split("\n")
    stopWords = []
    for w in stopWordFile:
        stopWords.append(w[0:-1])
    stopWords = stopWords[0:-1]
    return stopWords
def removeStopWords(pText):
    pText = removeWords(pText,getStopWords())
    return pText
def removeWords(pText,pWords):
    for w in (pWords):  
        pText.replace(w," ")
    return pText
def steam():
    ps = PorterStemmer()
    text = "Hola como estas consultado afijos eliminación"
    words = word_tokenize(text)
    for w in words:
        print(ps.stem(w))
def steamS(pText):
    #text = "Hola como estas consultado afijos eliminación torneos chico"
    text = pText
    stemmer = SnowballStemmer('spanish')
    stemmed_text = [stemmer.stem(i) for i in word_tokenize(text)]
    return stemmed_text
def deleteTildes(pText):
    pText = pText.replace("Ã¡","a").replace("Ã©","e").replace("Ã­","i").replace("Ã³","o").replace("Ãº","u")
    return pText
def removeTags(pText):
    p = re.compile('<([^<>])*>')
    pText = p.sub(" ",pText)
    pText = p.sub(" ",pText)
    p = re.compile('@import .*;')
    pText = p.sub(" ",pText)
    return pText
