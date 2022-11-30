# Jacob Burton Nov 2022
import requests
import csv
from bs4 import BeautifulSoup as bs

base_url = "https://en.wikipedia.org/wiki/"

print("Topic of Article to scrape:")

user_input = input()


## Wikipedia Python Search API
## Retrieved from https://www.mediawiki.org/wiki/API:Opensearch
S = requests.Session()

URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "opensearch",
    "namespace": "0",
    "search": user_input,
    "limit": "5",
    "format": "json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

page_url = DATA[3][0]


## Scrape for all links
requested_page = requests.get(page_url)
soup = bs(requested_page.text, 'html.parser')

foundlinks = soup.findAll('a', attrs={'class':'mw-redirect'})


## Format links
links = []
links.append(page_url)
for link in foundlinks:
    link = link.get('href')
    if link[0] != 'h':
        links.append('https://en.wikipedia.org' + link)
    else:
        links.append(link) ## already an http(s)

links = list(set(links)) ## remove duplicates


## Save results to file
filename = user_input.replace(' ', "_") + '.csv'

file = open(filename, 'w')
writer = csv.writer(file)

writer.writerow(links)

file.close()
