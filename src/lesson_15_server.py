import asyncio
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config_alfavantage import ALPHAVANTAGE_KEY  # isort:skip

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)


class CurrencyPair(BaseModel):
    from_currency: str
    to_currency: str


class RateResponse(BaseModel):
    rate: float


@dataclass
class CachedItem:
    rate: float
    timestamp: datetime


class Cacher:
    def __init__(self, cache_timeout=10):
        self.__locker = asyncio.Lock()
        self.__storage = {}
        self.__cache_timeout = cache_timeout

    async def get_item(self, key: str) -> Optional[float]:
        async with self.__locker:
            if key in self.__storage:
                item = self.__storage[key]
                if datetime.now() - item.timestamp < timedelta(seconds=self.__cache_timeout):
                    return item.rate
            return None

    async def put_item(self, key: str, rate: float):
        async with (self.__locker):
            self.__storage[key] = CachedItem(rate, datetime.now())


cacher = Cacher()


@app.post("/fetch-market")
async def get_current_market_state(currency_pair: CurrencyPair):
    """
    Fetches the current exchange rate between two currencies.

    Args:
        currency_pair: request model holding the "from_currency" and "to_currency" values.

    Returns:
        dict: A dictionary containing the exchange rate under the key "rate".
    """
    key = f"{currency_pair.from_currency}_{currency_pair.to_currency}"

    rate = await cacher.get_item(key)
    if rate:
        return RateResponse(rate=rate)
    url = (
        f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency_pair.from_currency}"
        f"&to_currency={currency_pair.to_currency}&apikey={ALPHAVANTAGE_KEY}"
    )

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            rate = float(data["Realtime Currency Exchange Rate"]["5. Exchange Rate"])
            await cacher.put_item(key, rate)
            return RateResponse(rate=rate)
        else:
            print(f"Error fetching exchange rate: {response.status_code}")
            raise HTTPException(status_code=400, detail="Failed to fetch exchange rate")
