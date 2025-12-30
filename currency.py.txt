import requests

def convert_to_sgd(amount, currency):
    if currency == "SGD":
        return amount

    url = "https://api.exchangerate.host/latest"
    params = {"base": currency, "symbols": "SGD"}
    response = requests.get(url, params=params).json()
    return amount * response["rates"]["SGD"]
