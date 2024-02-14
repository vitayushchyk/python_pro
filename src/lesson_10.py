import json
from dataclasses import dataclass
from datetime import datetime

import requests

ALPHAVANTAG_KEY = "SX3QUJZ4Q0FB9TNK"
MIDDLE_CURRENCY = "CHF"


@dataclass
class Price:
    value: float
    currency: str

    def __add__(self, other: "Price") -> "Price":
        if self.currency == other.currency:
            return Price(value=self.value + other.value, currency=self.currency)

        result = convert(self, MIDDLE_CURRENCY) + convert(other, MIDDLE_CURRENCY)
        return convert(result, self.currency)

    def __sub__(self, other: "Price") -> "Price":
        return self.__add__(Price(-other.value, other.currency))

    def __round__(self, ndigits=2):
        rounded_value = round(self.value, ndigits)
        return Price(rounded_value, self.currency)


def convert(price: Price, target_currency: str) -> Price:
    coefficient: float = 42.0
    #  this construct is used when alphavantage stops responding to requests
    try:
        response: requests.Response = requests.get(
            f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={price.currency}"
            f"&to_currency={target_currency}&apikey={ALPHAVANTAG_KEY}"
        )
        result: dict = response.json()
        coefficient = float(
            result["Realtime Currency Exchange Rate"]["5. Exchange Rate"],
        )
    except Exception as e:
        print("Oh no..... They want money from me ;( ", e)

    json_data: dict = {"result": []}
    with open("logs.json", "r+", encoding="utf-8", errors="replace") as f:
        if content := ''.join(f.readlines()):
            json_data = json.loads(content)
        json_data['result'].append(
            {
                "currency_from": price.currency,
                "currency_to": target_currency,
                "rate": coefficient,
                "timestamp": datetime.now().isoformat(),
            }
        )
        f.seek(0)
        json.dump(json_data, f, indent=4)

    return Price(
        value=price.value * coefficient,
        currency=target_currency,
    )


flight = Price(value=200, currency="USD")
hotel = Price(value=1000, currency="EUR")

relax = Price(value=5000, currency="UAH")
food = Price(value=20, currency="USD")

total: Price = flight + hotel
total_1: Price = relax - food
print(round(total))
print(round(total_1))
