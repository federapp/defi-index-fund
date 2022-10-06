#%%
import pandas as pd
import json
import requests
import time
#%%
payload={}
headers = {
  'accept': 'application/json'
}
def get_market_data(coingecko_name,request_date):
    url = f"https://api.coingecko.com/api/v3/coins/{coingecko_name}/history?date={request_date}"
    response = requests.request("GET", url, headers=headers)
    json_response = json.loads(response.text)
    func_response = []
    if 'market_data' not in json_response:
        func_response.append(0)
        func_response.append(0)
    else:
        func_response.append(json_response['market_data']['current_price']['usd'])
        func_response.append(json_response['market_data']['market_cap']['usd'])
    return func_response

#%%
asset_list = pd.read_csv('eligible_constituents.csv')

#%%
historical_data = pd.DataFrame()
historical_data.insert(0,'asset','')
historical_data.insert(1,'coingecko_name','')
historical_data.insert(2,'timestamp','')
historical_data.insert(3,'price','')
historical_data.insert(4,'market_cap','')

# %%
timestamp_list = []
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
year_list = ['2020','2021','2022']
for i in range(3):
    for j in range(12):
        timestamp_list.append(f'01-{month_list[j]}-{year_list[i]}')
# %%

for i in range(len(asset_list)):
    asset = asset_list.loc[i].asset
    coingecko_name = asset_list.loc[i].coingecko_name
    print(asset_list.loc[i].asset)
    for j in range(len(timestamp_list)):
        timestamp = timestamp_list[j]
        current_market_data = get_market_data(coingecko_name,timestamp)
        price = current_market_data[0] 
        market_cap = current_market_data[1] 
        historical_data.loc[len(historical_data.index)] = [asset,coingecko_name,timestamp,price,market_cap]
        print([asset,coingecko_name,timestamp,price,market_cap])
        time.sleep(8)
# %%
historical_data.to_csv('monthly_market_data.csv',index=False)
