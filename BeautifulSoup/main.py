import requests
from bs4 import BeautifulSoup
from queue import Queue
from collections import deque

# "Header" file - Define Adj. List class AND get beautifulsoup working

class AdjList:

    # Values
        # Start URL
    startURL = ""
        # End URL
    endURL = ""
        # Dictionary string : list
    dictURL = {}
        # URL : outURLs
    # Methods
        # Constructor (whatever that is)
    def __init__(self, startURL, endURL):
        self.startURL = startURL
        self.endURL = endURL

        # Print dict? debugging??
    def __str__(self):
        return self.dictURL

    def printDict(self):
        print("Keys: " + str(self.dictURL.keys()))
        print("Values: " + str(self.dictURL.values()))
        # print(self.dictURL)

        # Build Adj. List
    def buildAdjList(self):
        # URL queues: forward searches from start, backwards searches from end
        forwURL = self.startURL
        backwURL = self.endURL
        print(forwURL)
        print(backwURL)
        fwQueue = deque()
        bwQueue = Queue()
        fwSet = set(forwURL)
        bwSet = set(backwURL)

        # starting queues
        fwQueue.append(forwURL)
        bwQueue.put(backwURL)

        while bwQueue.empty() is False:
            # assign new current url
            forwURL = fwQueue.popleft()
            bwURL = bwQueue.get()
            print("Queue forward: " + forwURL)
            print("Queue backward: " + bwURL)

            fOutURL = []
            bOutURL = []

            f = requests.get(forwURL)
            b = requests.get(bwURL)
            fSoup = BeautifulSoup(f.text, 'html.parser')
            bSoup = BeautifulSoup(b.text, 'html.parser')

            if fSoup.find('p', class_='infobox ib-country vcard'):
                print("Skip countries")
                continue
            if fSoup.find('p', class_='infobox ib-settlement vcard'):
                print("Skip settlements")
                continue
            if bSoup.find('p', class_='infobox ib-country vcard'):
                print("Skip countries")
                continue
            if bSoup.find('p', class_='infobox ib-settlement vcard'):
                print("Skip settlements")
                continue

            # class_ = infobox ib-country vcard
            # search START wiki page, collect all URLS
            for a_tag in fSoup.find_all('a', href=True):
                # except if it's in the references or notes
                if a_tag.find(class_='reflist'):
                    break
                # or in categories
                if a_tag.find(class_='catlinks'):
                    break
                # or in the navigation box
                if a_tag.find(class_='navbox'):
                    break

                href = a_tag['href']
                if href.startswith("/wiki/") and not ":" in href:
                    # exclude links to the main page
                    if href == "/wiki/Main_Page":
                        continue
                    # or links to itself
                    if href is self.startURL:
                        continue
                    # or citations
                    if href.endswith("_(identifier)"):
                        continue
                    # or disambiguations (typically lists)
                    if href.endswith("_(disambiguation)"):
                        continue
                    # or lists
                    if href.startswith("/wiki/List_of"):
                        continue
                    finalOutURL = "https://en.wikipedia.org" + href
                    if finalOutURL == self.endURL:
                        print("Path found!")
                        print(finalOutURL)
                        fOutURL.append(finalOutURL)
                        fwSet.add(finalOutURL)
                        self.dictURL[forwURL] = fOutURL
                        return
                    # try to not have duplicates
                    if finalOutURL not in fwSet:
                        fOutURL.append(finalOutURL)
                        # if theres a similar article between the two searches
                        # if finalOutURL in bwSet:
                        #     # assign priority to checking those articles
                        #     fwQueue.clear()
                        #     fwQueue.appendleft(finalOutURL)
                        # else:
                        fwQueue.append(finalOutURL)
                    fwSet.add(finalOutURL)
            # Link current (forward) URL to its out URLs, add to list
            self.dictURL[forwURL] = fOutURL

            # Do it again, but this time from END wiki page
            for a_tag in bSoup.find_all('a', href=True):
                # except if it's in the references or notes
                if a_tag.find(class_='reflist'):
                    break
                # or in categories
                if a_tag.find(class_='catlinks'):
                    break
                # or in the navigation box
                if a_tag.find(class_='navbox'):
                    break

                hRef = a_tag['href']
                if hRef.startswith("/wiki/") and not ":" in hRef:
                    # exclude links to the main page
                    if hRef == "/wiki/Main_Page":
                        continue
                    # or links to itself
                    if hRef is self.startURL:
                        continue
                    # or citations
                    if hRef.endswith("_(identifier)"):
                        continue
                    # or disambiguations (typically lists)
                    if hRef.endswith("_(disambiguation)"):
                        continue
                    # or lists
                    if hRef.startswith("/wiki/List_of"):
                        continue
                    finalURL = "https://en.wikipedia.org" + hRef
                    if finalURL not in bwSet:
                        bOutURL.append(finalURL)
                        bwQueue.put(finalURL)
                    bwSet.add(finalURL)
            # Link current (backwards) URL to its out URLs, add to list
            self.dictURL[backwURL] = bOutURL

            if bwSet.isdisjoint(fwSet) is False:
                # print("Intersection:")
                intersect = bwSet.intersection(fwSet)
                for x in intersect:
                    string = x
                # print(string)
                fwQueue.clear()
                fwQueue.appendleft(string)
                fwSet.remove(string)
                bwSet.remove(string)
                intersect.clear()
            #     # print("page done, adding URLS to dict")
            #     # print(forwURL + ":  " + str(outURLs))

            if len(self.dictURL) > 10000:
                print("No path exists!")
                return


def main():
    adjlist = AdjList("https://en.wikipedia.org/wiki/Cat", "https://en.wikipedia.org/wiki/Stupidity")
    adjlist.buildAdjList()
    print("Finally done.")
    print("Final product: ")
    adjlist.printDict()

if __name__ == "__main__":
    main()

