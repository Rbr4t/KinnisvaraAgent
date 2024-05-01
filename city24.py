import requests
import os
import json
import random

# Accessing the API
url = "https://api.city24.ee/et_EE/search/realties?address%5Bcc%5D=1&address%5Bcity%5D%5B%5D=20411&tsType=rent&unitType=Apartment&adReach=1&itemsPerPage=50&page=1"
headers_file = open("user_agents.txt", "r")
headers = headers_file.readlines()
headers_file.close()

resp = requests.get(
    url, headers={"User-Agent": headers[random.randint(0, 1000)].strip()})
full_data = []
for d in resp.json():

    # More info can be extracted with more attributes
    obj = {
        "price": d["price"],
        "area": d["property_size"],
        "rooms": d["room_count"],
        "permalink": "https://www.city24.ee/real-estate/" + d["friendly_id"],
    }
    full_data.append(obj)

print(len(full_data))
json_object = json.dumps(full_data, indent=4)

os.remove("korteridCity.json")
with open("korteridCity.json", "w") as outfile:
    json.dump([], outfile)
    outfile.write(json_object)
