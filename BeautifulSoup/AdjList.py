import aiohttp
import asyncio
import time
import breadthFirstSearch
import depthFirstSearch
from bs4 import BeautifulSoup
from queue import Queue
from collections import deque

# "Header" file
# Wikigame list of rules: https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game
class AdjList:

    # Values
        # Start URL
    startURL = ""
        # End URL
    endURL = ""
        # Dictionary string : list, URL : outURLs
    dictURL = {}

    # Methods
        # Constructor
    def __init__(self, startURL, endURL):
        self.startURL = startURL
        self.endURL = endURL

    def __str__(self):
        return self.dictURL

        # Prints all keys and values. Value lists are so large... quite hard to read...
    def printDict(self):
        print("Keys: " + str(self.dictURL.keys()))
        print("Values: " + str(self.dictURL.values()))

    def searches(self):
        breadthFirstSearch.bfs(self.dictURL, self.startURL, self.endURL)
        depthFirstSearch.dfs(self.dictURL, self.startURL, self.endURL)

        # Build Adj. List
    async def buildAdjList(self, start_time):
        print("Building list, please wait...")
        # Initializing Queue - quick explanation
            # URL queues: forward searches from start, backwards searches from end.
            # Backwards simulates priority. If the forward queue comes across one of the backwards pages,
            # The queue will prioritize that page, as its more likely to point towards the end URL
            # So the "random" search becomes more directed.
        # Start and end URLs
        forwURL = self.startURL
        backwURL = self.endURL
        # Forwards deque (functions as a normal queue, but can add things to the front for prioritization)
        # Backwards queue is just a normal queue.
        fwQueue = deque()
        bwQueue = Queue()
        # Tracks whether these pages have been visited yet. Add initial pages.
        fwSet = set(forwURL)
        bwSet = set(backwURL)

        # Starting queues
        fwQueue.append(forwURL)
        bwQueue.put(backwURL)
        # External session - Quicker fetch times
        session = aiohttp.ClientSession()

        while bwQueue.empty() is False:
            # Assign new current url
            if len(fwQueue) > 0:
                forwURL = fwQueue.popleft()
            else:
                # If the queue empties, there probably isn't a path
                print("Queue empty. List could not be completed.")
                await session.close()
                return

            bwURL = bwQueue.get()
            # If the URL was already visited, keep moving
            if forwURL in fwSet:
                continue
            if bwURL in bwSet:
                continue
            # Mark as visited
            fwSet.add(forwURL)
            bwSet.add(bwURL)
            # All URLs from the page
            fOutURL = []
            bOutURL = []

            # Load page content
            async with session.get(forwURL) as resp:
                f = await resp.text()
            async with session.get(bwURL) as response:
                b = await response.text()

            fSoup = BeautifulSoup(f, 'html.parser')
            bSoup = BeautifulSoup(b, 'html.parser')

            # If either page is for a country or town, skip
            # Countries/towns/locations have way too many links
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

            # Pull all links from page in the forward queue
            for a_tag in fSoup.find_all('a', href=True):
                # except if it's in the references or notes
                if a_tag.find(class_='reflist'):
                    continue
                # or in categories
                if a_tag.find(class_='catlinks'):
                    continue
                # or in the navigation box
                if a_tag.find(class_='navbox'):
                    continue
                # ^(Can't use these in the wiki game)

                href = a_tag['href']
                # No external links
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
                    # or lists - can't use in the wikigame
                    if href.startswith("/wiki/List_of"):
                        continue
                    # Put link in URL format
                    finalOutURL = "https://en.wikipedia.org" + href
                    # If the link hasn't been visited yet
                    if finalOutURL not in fwSet:
                        # Add to this page's outgoing links list
                        fOutURL.append(finalOutURL)
                        # If there's a similar article between the two searches
                        if finalOutURL in bwSet:
                            # Prioritize searching that link, probably closer to target
                            fwQueue.clear()
                            fwQueue.appendleft(finalOutURL)
                        # Otherwise, add to queue like normal
                        else:
                            fwQueue.append(finalOutURL)
            # Link current page to its out URLs, add to list
            self.dictURL[forwURL] = fOutURL

            # Do it again, but this time from END wiki page
            for a_tag in bSoup.find_all('a', href=True):
                if a_tag.find(class_='reflist'):
                    continue
                if a_tag.find(class_='catlinks'):
                    continue
                if a_tag.find(class_='navbox'):
                    continue

                hRef = a_tag['href']
                if hRef.startswith("/wiki/") and not ":" in hRef:
                    if hRef == "/wiki/Main_Page":
                        continue
                    if hRef is self.startURL:
                        continue
                    if hRef.endswith("_(identifier)"):
                        continue
                    if hRef.endswith("_(disambiguation)"):
                        continue
                    if hRef.startswith("/wiki/List_of"):
                        continue
                    finalURL = "https://en.wikipedia.org" + hRef
                    # If the link hasn't been visited yet, add it to queue
                    if finalURL not in bwSet:
                        bOutURL.append(finalURL)
                        bwQueue.put(finalURL)
                        # No need for prioritization
            # Link current page to its out URLs, add to list
            self.dictURL[backwURL] = bOutURL

            # If the goal is found in any of the children links, mission accomplished
            if self.endURL in fOutURL:
                print("List complete.")
                await session.close()
                return
            # If it takes too long, there probably isn't a path
            cycle_time = time.time()
            if (cycle_time - start_time) > 300:
                print("Session timed out. List could not be completed.")
                await session.close()
                return
        # Or if the queue empties, there probably isn't a path
        print("Queue empty. List could not be completed.")
        await session.close()
        return


async def main():
    # Takes start URL and end URL
    adjlist = AdjList("https://en.wikipedia.org/wiki/Fortnite", "https://en.wikipedia.org/wiki/Sweaty")
    # Start timer - tracks how long the list takes to build
    start_time = time.time()
    await adjlist.buildAdjList(start_time)
    print("Time: " + str(round(time.time()-start_time, 2)) + " seconds.")
    adjlist.searches()
    #adjlist.printDict()

# Aiohttp stuff, do not touch!!
loop = asyncio.get_event_loop() # Will throw a warning, but it's fine
loop.run_until_complete(main())
# REF: https://oxylabs.io/blog/asynchronous-web-scraping-python-aiohttp
# REF: https://docs.aiohttp.org/en/stable/client_quickstart.html
