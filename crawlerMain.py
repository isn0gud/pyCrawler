import sys
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from builtins import print
from collections import OrderedDict
import math

__author__ = 's0540030,s0540040,s054XXX'

d = 0.95
t = 0.05
delta = 0.04
iterSites = 4


def sum1(pi, graph, ranks, linkCount, currentIteration):
    summe = 0
    indexOfPj = 0
    for pj in graph:
        listOflinksOfPj = graph.get(pj)
        if pi in listOflinksOfPj:
            summe += ranks[currentIteration - 1][indexOfPj] / len(graph.get(pj))
        indexOfPj = indexOfPj + 1
    return summe


def sum2(graph, ranks, currentIteration):
    summe = 0
    indexOfPj = 0
    for pj in graph:
        if (len(graph.get(pj)) == 0):
            summe += ranks[currentIteration - 1][indexOfPj] / len(graph)
        indexOfPj = indexOfPj + 1
    return summe


def pageRank(graph, ranks):
    for site in range(len(ranks[0])):
        ranks[0][site] = 1 / (len(graph))
    for step in range(1, iterSites):
        linkNum = 0
        for link in graph.keys():
            ranks[step][linkNum] = d * (sum1(link, graph, ranks, linkNum, step) + sum2(graph, ranks, step)) + t / len(
                graph)
            linkNum += 1


def makeIndex(sites):
    index = dict()

    wordsWithOrigin = list()
    for site in sites:
        file = request.urlopen(site)
        soup = BeautifulSoup(file)
        text = soup.get_text()
        words = text.lower().split()
        punctuationMarks = ['!', ',', '.', ':', '"', '?', '-', ';', '(', ')', '[', ']', '\\', '/']
        stopWords = ['d01', 'd02', 'd03', 'd04', 'd05', 'd06', 'd07', 'd08',
                     'a', 'also', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'do',
                     'for', 'have', 'is', 'in', 'it', 'of', 'or', 'see', 'so',
                     'that', 'the', 'this', 'to', 'we']
        for word in words:
            for mark in punctuationMarks:
                if mark in word:
                    word = word.replace(mark, "")
            if word not in stopWords:
                wordsWithOrigin.append((word, site))
    for word in wordsWithOrigin:
        if word[0] not in index:
            index[word[0]] = list()
            index[word[0]].append(1)
            index[word[0]].append(dict())
            index[word[0]][1][word[1]] = 1
        else:
            if word[1] not in index[word[0]][1]:
                index[word[0]][1][word[1]] = 1
                index[word[0]][0] += 1
            else:
                index[word[0]][1][word[1]] += 1
    return index


def getResultsWithScore(searchTerm, index, numberOfDocuments):
    termList = createTermListFromSearchTerm(searchTerm)
    searchVector = createVectorForSearchTerm(termList, index, numberOfDocuments)
    listOfDocuments = getListOfDocumentsContainingTerms(termList, index)
    resultList = list()
    for document in listOfDocuments:
        documentVector = createVectorForDocument(document, index, numberOfDocuments)
        score = calculateScore(documentVector, searchVector)
        entry = list()
        entry.append(score)
        entry.append(document)
        resultList.append(entry)

    sorted(resultList, key=lambda result: result[0])  #Sort by score
    return resultList


def createTermListFromSearchTerm(searchTerm):
    termList = searchTerm.lower().split()
    punctuationMarks = ['!', ',', '.', ':', '"', '?', '-', ';', '(', ')', '[', ']', '\\', '/']
    for term in termList:
        for mark in punctuationMarks:
            if mark in term:
                term = term.replace(mark, "")
    return termList


def getListOfDocumentsContainingTerms(termList, index):
    listOfDocuments = list()
    for term in termList:
        if term in index:
            for document in index[term][1].keys():
                if document not in listOfDocuments:
                    listOfDocuments.append(document)
    return listOfDocuments


def calculateScore(documentVector, searchVector):
    numerator = 0
    documentDenominator = 0
    searchDenominator = 0
    for i in range(0, len(documentVector) - 1):

        numerator = numerator + (documentVector[i] * searchVector[i])
        documentDenominator += math.pow(documentVector[i], 2)
        searchDenominator += math.pow(searchVector[i], 2)
    documentDenominator = math.sqrt(documentDenominator)
    searchDenominator = math.sqrt(searchDenominator)
    denominator = searchDenominator * documentDenominator
    return numerator / denominator


def createVectorForSearchTerm(termList, index, numberOfDocuments):
    vector = list()
    for term in index:
        if term in termList:
            vector.append(getTermWeight(term, termList, index, numberOfDocuments))
        else:
            vector.append(0)
    return vector

def getTermWeight(term, termList, index, numberOfDocuments):
    return getDocumentFrequencyWeight(term, index, numberOfDocuments) * getTermFrequencyWeight(term, termList)


def getTermFrequencyWeight(term, termList):
    termCount = getTermCount(term, termList)
    if termCount == 0:
        return 0
    else:
        return 1 + math.log(termCount, 10)


def getTermCount(term, termList):
    returnValue = 0
    for t in termList:
        if t == term:
            returnValue += 1
    return returnValue


def createVectorForDocument(document, index, numberOfDocuments):
    vector = list()
    for term in index:
        if document in index[term][1]:
            vector.append(getTermWeightInDocument(term, document, index, numberOfDocuments))
        else:
            vector.append(0)
    return vector


def getTermWeightInDocument(term, document, index, numberOfDocuments):
    return getDocumentFrequencyWeight(term, index, numberOfDocuments) * getTermFrequencyWeightInDocument(term, document,
                                                                                                         index)


def getDocumentFrequencyWeight(term, index, numberOfDocuments):
    return math.log(numberOfDocuments / getDocumentFrequency(term, index), 10)


def getDocumentFrequency(term, index):
    if term in index:
        return index[term][0]
    else:
        return 0


def getTermFrequencyWeightInDocument(term, document, index):
    termFrequency = getTermFrequencyInDocument(term, document, index)
    if termFrequency == 0:
        return 0
    else:
        return 1 + math.log(termFrequency, 10)


def getTermFrequencyInDocument(term, document, index):
    if term in index:
        if document in index[term][1]:
            return index[term][1][document]
        else:
            return 0
    else:
        return 0


def combineSearchPageRank(searchResults, ranks, graph):
    for i in range(0, len(searchResults) - 1):
        #print(searchResults[i][1] + " = " + list(graph.keys())[list(graph.keys()).index(searchResults[i][1])] )
        searchResults[i][0] = searchResults[i][0] * ranks[3][list(graph.keys()).index(searchResults[i][1])]
       
def getKey(item):
    return item[0] 

def main(argv):
    listToVisit = ["http://mysql12.f4.htw-berlin.de/crawl/d01.html",
                   "http://mysql12.f4.htw-berlin.de/crawl/d06.html",
                   "http://mysql12.f4.htw-berlin.de/crawl/d08.html"]
    listVisited = []
    graph = dict()
    #crawler
    while listToVisit:
        url = listToVisit.pop()
        file = request.urlopen(url)
        listVisited.append(url)
        graph[url] = list()
        soup = BeautifulSoup(file)
        for link in soup.find_all('a'):
            newUrl = link.get('href')
            newUrl = parse.urljoin(url, newUrl)
            if (url in graph) and not (newUrl == url):
                graph[url].append(newUrl)
            else:
                graph[url] = list([newUrl])
            if not (newUrl in listToVisit) and not (newUrl in listVisited): listToVisit.append(newUrl)
    graph = OrderedDict(sorted(graph.items(), key=lambda t: t[0]))
    ranks = [[0 for y in range(0, len(graph))] for x in range(0, iterSites)]
    pageRank(graph, ranks)
    index = makeIndex(listVisited)
    index = OrderedDict(sorted(index.items(), key=lambda t: t[0]))   
    searchTerm = str(sys.argv[1]);
    if (str(sys.argv[2]) != ""):
        searchTerm += " " + str(sys.argv[2]);
    print(searchTerm + ":")
    resultList = getResultsWithScore(searchTerm, index, len(listVisited))
    #for item in resultList:
    #    print(item)
    #print("----")
    combineSearchPageRank(resultList, ranks, graph)
    resultList.sort(key=getKey, reverse=True)
    for item in resultList:
        print(item)
if __name__ == "__main__": main(sys.argv)




