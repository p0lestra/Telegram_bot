import requests
import json

from config import keys, api


class APIException(Exception):
    pass


class MoneyConverter:
    @staticmethod
    def get_price(to: str, base: str, amount: str):
        if to == base:
            raise APIException(f'Не удалось перевести одинаковые валюты {base}')

        try:
            to_ticker = keys[to]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {to}')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(
            f"https://api.apilayer.com/exchangerates_data/convert?to={to_ticker}&from={base_ticker}&amount={amount}",
            headers=api)
        total = json.loads(r.content)['result']
        print(f'{total}')

        return total
