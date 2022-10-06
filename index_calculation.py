#%%
import pandas as pd
import json

#%%
df = pd.read_csv('monthly_market_data.csv')
monthly_performance = pd.DataFrame()
monthly_performance.insert(0,'timestamp','')
monthly_performance.insert(1,'delta','')

#%%
timestamp_list = []
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
year_list = ['2020','2021','2022']
for i in range(3):
    for j in range(12):
        timestamp_list.append(f'01/{month_list[j]}/{year_list[i]}')
# %%
final_value = 1
for i in range (len(timestamp_list) - 1):
    current_timestamp = timestamp_list[i]
    next_timestamp = timestamp_list[i+1]
    current_timestamp_df = df[df['timestamp']==current_timestamp]
    next_timestamp_df = df[df['timestamp']==next_timestamp]

    current_timestamp_df.sort_values('market_cap',ascending=False,inplace=True)
    current_top_assets = current_timestamp_df.head(5)

    current_total_market_cap = current_top_assets['market_cap'].sum()
    current_top_assets["weight"] = current_top_assets["market_cap"] / current_total_market_cap

    current_top_assets = current_top_assets.merge(next_timestamp_df[['asset','price']],on='asset',how='left')

    current_top_assets["price_delta"] = (current_top_assets["price_y"] / current_top_assets["price_x"]) - 1
    current_top_assets["weighted_price_delta"] = current_top_assets["weight"] * current_top_assets["price_delta"]

    monthly_delta = current_top_assets['weighted_price_delta'].sum()

    monthly_performance.loc[len(monthly_performance.index)] = [current_timestamp,monthly_delta]

# %%
monthly_performance.to_csv('monthly_performance.csv',index=False)
# %%
