import requests


def get_symbol_price(symbol):
    url = f"https://api.bybit.com/v2/public/tickers?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    if data["ret_code"] == 0:
        return data["result"][0]["last_price"]
    else:
        return None

