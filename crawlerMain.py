from bs4 import BeautifulSoup
from urllib.parse import urlparse
__author__ = 's0540030'

def main():
    print("Starte Parser")
    file = urlparse("http://mysql12.f4.htw-berlin.de/crawl/d01.html")

    soup = BeautifulSoup(file)
    tag = soup.find("br/>")
    print("Ausgabe")
    print(tag)




main()