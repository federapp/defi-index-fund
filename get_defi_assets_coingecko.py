import bs4
import pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.coingecko.com/en/categories/decentralized-finance-defi"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}
r = requests.get(url,
                 timeout=10,
                 headers=headers)

df = pd.DataFrame()
df.insert(0,'asset','')
df.insert(1,'coingecko_name','')

soup = BeautifulSoup(r.content,'html.parser')
asset_list = soup.find_all('a',{"class": "tw-flex tw-items-start md:tw-flex-row tw-flex-col"})

splitted_list = asset_list[0].text.splitlines()
asset = list(filter(None, splitted_list))[-1]
coingecko_name = asset_list[0]['href'].split('/')[-1]

for i in range (len(asset_list)):
    splitted_list = asset_list[i].text.splitlines()
    asset = list(filter(None, splitted_list))[-1]
    coingecko_name = asset_list[i]['href'].split('/')[-1]

    df.loc[i] = [asset,coingecko_name]

df.to_csv('asset_list.csv',index=False)
