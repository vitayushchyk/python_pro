class Price:
    _CURRENCIES = {
        "CHF": 1,
        "UAH": 0.023,
        "USD": 0.87,
        "EUR": 0.94,
    }

    def __init__(self, value: float, currency: str) -> None:
        if currency not in self._CURRENCIES:
            raise ValueError(f"Please select one of the available currencies: {', '.join(self._CURRENCIES.keys())}")
        self.value: float = value
        self.currency: str = currency

    @property
    def normalized(self):
        return self.value * self._CURRENCIES[self.currency]

    def __add__(self, other: "Price") -> "Price":
        return Price(
            value=(self.normalized + other.normalized) / self._CURRENCIES[self.currency], currency=self.currency
        )

    def __sub__(self, other: "Price") -> "Price":
        return Price(
            value=(self.normalized - other.normalized) / self._CURRENCIES[self.currency],
            currency=self.currency,
        )

    def __str__(self):
        return f'Price is {self.value} {self.currency}'

    # I added this method because I'm annoyed by many values after the dot.
    def __round__(self, ndigits=2):
        rounded_value = round(self.value, ndigits)
        return Price(rounded_value, self.currency)


flight = Price(value=200, currency="USD")
hotel = Price(value=1000, currency="EUR")

relax = Price(value=5000, currency="UAH")
food = Price(value=20, currency="USD")

total: Price = flight + hotel
total_1: Price = relax - food
# total.currency == USD
# total.currency == UAH
print(round(total))
print(round(total_1))
