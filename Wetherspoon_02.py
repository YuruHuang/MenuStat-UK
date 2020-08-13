import json
import requests
from datetime import date
import pandas as pd
import os

path_wetherspoon = './wetherspoon_' + date.today().strftime("%b-%d-%Y")
os.mkdir(path_wetherspoon)


def wetherspoonCrawler(pub_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'APIKey': 'YVB5QfeRKUK1+EGvXGjPgQA93reRTUJHsCuQSHR+=='}
    url = f'https://www.jdwetherspoon.com//api/v2/pubs/{pub_id}/food'
    resp = requests.get(url, headers=headers)
    items = resp.json()
    fileName = path_wetherspoon + '/pub_' + str(pub_id) + '.json'
    with open(fileName, 'w') as f:
        json.dump(items, f)
    pd.DataFrame(items).to_csv(path_wetherspoon + '/pub_' + str(pub_id) + '.csv')
    print('Finished Scraping Wetherspoon:' + str(pub_id))

wetherspoon = wetherspoonCrawler(pub_id=70)

