import aiohttp
import asyncio
import time
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

        # Build Adj. List
    async def buildAdjList(self, start_time):
        print("Building list, please wait...")

        # External session - Quicker fetch times
        session = aiohttp.ClientSession()

        # Initializing Queue - quick explanation
            # URL queues: forward searches from start, backwards searches from end.
            # Backwards simulates priority. If the forward queue comes across one of the backwards pages,
            # The queue will prioritize that page, as its more likely to point towards the end URL
            # So the "random" search becomes more directed.

        # Validating links
        # Open page at link (sometimes, an inputted link is redirected to a different page)
        async with session.get(self.startURL) as response:
            s = await response.text()
        async with session.get(self.endURL) as resp:
            e = await resp.text()

        sSoup = BeautifulSoup(s, "html.parser")
        eSoup = BeautifulSoup(e, "html.parser")

        # Get the link of the page (whether its the same link inputted or the redirected one)
        forwURL = sSoup.find('link', rel="canonical")['href']
        backwURL = eSoup.find('link', rel="canonical")['href']
        # And set as the correct links to search from and for
        self.startURL = forwURL
        self.endURL = backwURL

        # Forwards deque (functions as a normal queue, but can add things to the front for prioritization)
        # Backwards queue is just a normal queue.
        fwQueue = deque()
        bwQueue = Queue()
        # Tracks whether these pages have been visited yet. Add initial pages.
        fwSet = set(forwURL)
        bwSet = set(backwURL)
        # Priority
        priority = False

        # Starting queues
        fwQueue.append(forwURL)
        bwQueue.put(backwURL)

        while bwQueue.empty() is False:
            # Assign new current url
            if len(fwQueue) > 0:
                forwURL = fwQueue.popleft()
            else:
                # If the queue empties, there probably isn't a path
                print("Queue empty. List could not be completed.")
                await session.close()
                return

            backwURL = bwQueue.get()
            # If the URL was already visited, keep moving
            if forwURL in fwSet:
                continue
            if backwURL in bwSet:
                continue
            # Mark as visited
            fwSet.add(forwURL)
            bwSet.add(backwURL)
            # All URLs from the page
            fOutURL = []
            bOutURL = []

            # Load page content
            async with session.get(forwURL) as resp:
                f = await resp.text()
            async with session.get(backwURL) as response:
                b = await response.text()

            fSoup = BeautifulSoup(f, 'html.parser')
            bSoup = BeautifulSoup(b, 'html.parser')

            # If either page is for a country or town, skip
            # Countries/towns/locations have way too many links
            if fSoup.find('table', class_='infobox ib-country vcard') or fSoup.find('table', class_='infobox ib-settlement vcard'):
                print("Skip settlements and countries")
                continue
            if bSoup.find('table', class_='infobox ib-country vcard') or bSoup.find('table', class_='infobox ib-settlement vcard'):
                print("Skip settlements and countries")
                continue

            # Pull all links from page in the forward queue
            for a_tag in fSoup.find_all('a', href=True):
                # except if it's in the references or notes
                if a_tag.find(class_='reflist'):
                    print("meow")
                    continue
                # or in categories
                if a_tag.find(class_='catlinks'):
                    print("this works")
                    continue
                # or in the navigation box
                if a_tag.find(class_='navbox'):
                    print("yippeee")
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
                        if priority is True:
                            fwQueue.append(finalOutURL)
                        if finalOutURL in bwSet:
                            # Prioritize searching that link, probably closer to target
                            fwQueue.appendleft(finalOutURL)
                            priority = True
                        # Otherwise, add to queue like normal
                        else:
                            fwQueue.append(finalOutURL)
            # Link current page to its out URLs, add to list
            self.dictURL[forwURL] = fOutURL
            if priority is True:
                priority = False

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



# Aiohttp stuff, do not touch!!
loop = asyncio.get_event_loop() # Will throw a warning, but it's fine
loop.run_until_complete(main())
# REF: https://oxylabs.io/blog/asynchronous-web-scraping-python-aiohttp
# REF: https://docs.aiohttp.org/en/stable/client_quickstart.html

# Note: Instead of wiping the queue to prioritize, try saving a copy of the old queue somewhere and just moving up
# the prioritized articles