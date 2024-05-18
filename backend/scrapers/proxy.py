import random
import requests


def getProxy():
    with open("./scrapers/proxies.txt", "r") as file:
        file = file.readlines()

        random_selection = [file[x].strip()
                            for x in [random.randint(0, 5416) for x in range(10)]]
        i = 0
        try:
            resp = requests.get(
                "https://google.com", proxies={"http": f"http://{random_selection[i]}"})
        except IOError:
            i += 1
            pass
        else:
            return {"http": f"http://{random_selection[i]}"}
