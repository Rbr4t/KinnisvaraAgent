import requests
import re
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://www.kv.ee/search?orderby=ob&deal_type=2&county=12&parish=1063"

# This is how I'm going to extract more info for future development, that search url is going to give me all the necessary links
"""
url2 = "https://www.kv.ee/armas-privaatne-taiesti-omaette-sissepaasuga-korte-3059543.html"

page2 = requests.get(url2, headers=headers)
print()
y = open("output2.txt", "w")
y.write(page2.text)
y.close()
"""
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")
element = soup.find(
    "div", class_="results results-default").find_all("article")

full_data = []

for e in element:

    obj = {
        "rooms": int(e.find("div", class_="rooms").contents[0].strip()),
        "price": int(re.search(r'\d+', e.find("div", class_="price").contents[0].strip().split(r'"\d"')[0]).group()),
        "area": int(re.search(r'\d+', e.find("div", class_="area").contents[0].strip().split(r'"\d"')[0]).group()),
        "permalink":  "https://www.kv.ee" + e['data-object-url']
    }

    full_data.append(obj)
print(full_data)

# z = open("output.txt", "w")
# z.write(str(element))
# z.close()
