from curl_cffi import requests

cookies = {
    'INTRESS_PERCENT_EST': '6.1',
    'LVO': '3629551',
    'PHPSESSID': 'j5rta7bcj73ib4rdiahe9rviv172gnq1',
    '__cf_bm': 'KmjOqor86I0Y5B9akZSuER7gQ7vEn2Ponwcuy5jzdlU-1716289933-1.0.1.1-6yKQMg0bB8blL.cK3.iVzxXTAunlKkRMBPSeMqKIqWTGqeXDbFRP6pNSPQaHzcNn5aBGKfIU9xXZyJaO3.PmrA',
    'interest': '6.1',
    'list_view': 'default',
    'saved_searches': '2e4e74a12692ee7b2dff57022b1bf929',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}


response = requests.get(
    'https://www.kv.ee/search?orderby=ob&deal_type=2&limit=100&start=0&orderby=cdwl', impersonate="chrome101", cookies=cookies, headers=headers)
print(response.json())
