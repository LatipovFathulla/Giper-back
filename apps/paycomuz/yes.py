import requests

url = 'https://api.gipermart.uz/outside/exchange-rates/'
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    for rate in data:
        if rate['code'] == 'USD':
            cb_price = float(rate['nbu_buy_price'])
            break
    else:
        cb_price = 1.0
else:
    cb_price = 1.0

print("USD exchange rate:", int(cb_price))