import requests
import json
from config import keys

class ConvertException(Exception):
    pass

class ConvertionException:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        try:
            qticker = keys[quote]
        except KeyError:
            raise ConvertException(f'Неправильно введена валюта {quote}')

        try:
            bticker = keys[base]
        except KeyError:
            raise ConvertException(f'Неправильно введена валюта {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertException(f"Неправильно введено количество {amount}")

        if quote == base:
            raise ConvertException(f'Нельзя перевести одинаковые валюты {quote}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={qticker}&tsyms={bticker}')
        a = float(json.loads(r.content)[keys[base]])
        return a