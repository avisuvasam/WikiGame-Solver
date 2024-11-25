import requests
from bs4 import BeautifulSoup



r = requests.get("https://en.wikipedia.org/wiki/Albert_Einstein")
soup = BeautifulSoup(r.text, "html.parser")

for a_tag in soup.find_all("a", href=True):
    href = a_tag["href"]
    if href.startswith("/wiki/") and not ":" in href:
        print("href: ", href)

        """
        # Fetch the content of each linked page
        full_url = "https://en.wikipedia.org" + href
        linked_page = requests.get(full_url)
        print(linked_page.content[:500])  # Print the first 500 bytes of the content
        """


"""
base_url = "https://en.wikipedia.org/wiki/Albert_Einstein"

for a_tag in soup.find_all("a", class_="listing-name", href=True):
    print("-" * 60)
    print("href: ", a_tag["href"])
    request_href = requests.get(base_url + a_tag['href'])
    print(request_href.content)

"""
