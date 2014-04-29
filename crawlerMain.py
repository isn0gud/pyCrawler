import sys
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

__author__ = 's0540030,s0540040,s054XXX'

d = 0.95
t = 0.05
delta = 0.04
iter = 3

def sum1(pi, graph, ranks, i):
    summe = 0
    for pj in graph:
        print(pj)
       # if pj.contains(pi):
        #    sum += (ranks[i][graph.])


def pageRank(graph):
    ranks = [[0 for y in range(0,len(graph))] for x in range(0,iter)]
    for site in range(0, len(graph)):
        ranks[0][site] = 1/len(graph)
    for step in range(1,iter):
        linkNum = 0
        for link in graph.keys():
            ranks[step][linkNum] = d
            sum1(link, graph, ranks, linkNum)
            linkNum += 1




def main(argv):
    listToVisit = ["http://mysql12.f4.htw-berlin.de/crawl/d01.html",
               "http://mysql12.f4.htw-berlin.de/crawl/d06.html",
               "http://mysql12.f4.htw-berlin.de/crawl/d08.html"]


    listVisited = []
    graph = dict()
    while listToVisit:
        url = listToVisit.pop()
        file = request.urlopen(url)
        listVisited.append(url)
        soup = BeautifulSoup(file)
        for link in soup.find_all('a'):
            newUrl = link.get('href')
            newUrl = parse.urljoin(url, newUrl)
            if (url in graph) and not (newUrl == url):
                graph[url].append(newUrl)
            else:
                graph[url] = list([newUrl])
            if not (newUrl in listToVisit) and not (newUrl in listVisited): listToVisit.append(newUrl)
    for item in listVisited: print(item)
    pageRank(graph)
    print('\n')
    print(graph)
if __name__ == "__main__": main(sys.argv)




