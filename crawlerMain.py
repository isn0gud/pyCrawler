import sys
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from builtins import print
from collections import OrderedDict

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
            summe += ranks[currentIteration-1][indexOfPj]/len(graph.get(pj))
        indexOfPj = indexOfPj +1
    return summe

def sum2(graph, ranks, currentIteration):
    summe = 0
    indexOfPj = 0
    for pj in graph:
        if (len(graph.get(pj))==0):
            summe += ranks[currentIteration-1][indexOfPj]/len(graph)
        indexOfPj = indexOfPj +1
    return summe

def pageRank(graph, ranks):

    for site in range(len(ranks[0])):
        ranks[0][site] = 1/(len(graph))
    for step in range(1,iterSites):
        linkNum = 0
        for link in graph.keys():
            ranks[step][linkNum] = d * (sum1(link, graph, ranks, linkNum, step) + sum2(graph, ranks, step)) +t/len(graph)
            linkNum += 1

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
    ranks = [[0 for y in range(0,len(graph))] for x in range(0,iterSites)]
    pageRank(graph, ranks)
#print pagerank
    for row in ranks:
        print(row)
             
if __name__ == "__main__": main(sys.argv)




