from curl_cffi import requests
import json

maakonnad = [
    "Harju maakond",
    "Tartu maakond",
    "Ida-Viru maakond",
    "Pärnu maakond",
    "Lääne-Viru maakond",
    "Viljandi maakond",
    "Rapla maakond",
    "Võru maakond",
    "Saare maakond",
    "Jõgeva maakond",
    "Järva maakond",
    "Valga maakond",
    "Põlva maakond",
    "Lääne maakond",
    "Hiiu maakond"
]

big_ass_json = {}
for maakond in maakonnad:
    big_ass_json[maakond] = {}
    resp = requests.get(
        f"https://kinnisvara24.ee/adr/search/next-level?A1={maakond.replace(' ', '+')}")
    A2 = resp.json().get("A2", [])

    for vald in A2:
        print(vald)
        big_ass_json[maakond][vald] = {}

        resp = requests.get(
            f"https://kinnisvara24.ee/adr/search/next-level?A1={maakond.replace(' ', '+')}&A2={vald.replace(' ', '+')}")
        A3 = resp.json().get("A3", [])

        for linnaosa in A3:
            big_ass_json[maakond][vald][linnaosa] = []

            if "linn" in linnaosa and "linnaosa" not in linnaosa:
                resp = requests.get(
                    f"https://kinnisvara24.ee/adr/search/next-level?A1={maakond.replace(' ', '+')}&A2={vald.replace(' ', '+')}&A3={linnaosa.replace(' ', '+')}")
                A4 = resp.json().get("A4", [])
                big_ass_json[maakond][vald][linnaosa] = A4


with open("output.json", "w") as file:
    file.write(json.dumps(big_ass_json))
