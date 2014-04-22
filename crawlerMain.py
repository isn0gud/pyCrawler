import sys
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

__author__ = 's0540030,s0540040,s054XXX'

d = 0.95


def pageRank(graph):


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
    print('\n')
    print(graph)
if __name__ == "__main__": main(sys.argv)




