import datetime
import requests

import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()  # Finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found about

STOCK_URL = 'https://www.alphavantage.co/query'


class StockInfo:
    def __init__(self, stock: str):
        stock_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": {stock},
            "apikey": os.getenv("ALPHA_VANTAGE_KEY")  # Gets API Key from the .env
        }

        self.today, self.yesterday = self.get_dates()
        self.stock_request = requests.get(STOCK_URL, stock_params)
        self.stock_request.raise_for_status()

    @staticmethod
    def get_dates():
        """ Gets today's and yesterday's dates as strings"""
        today_date = str(datetime.date.today() - datetime.timedelta(days=1))
        yesterday_date = str(datetime.date.today() - datetime.timedelta(days=2))
        return today_date, yesterday_date

    def find_change(self):
        """
        Gets the values of today's and yesterday's opening price then returns the percent change
        :return: The percentage of change in price
        """

        today_open = float(self.stock_request.json()["Time Series (Daily)"][self.today]["1. open"])
        yesterday_open = float(self.stock_request.json()["Time Series (Daily)"][self.yesterday]["1. open"])
        change = today_open - yesterday_open
        percent_change = (change / abs(yesterday_open)) * 1000
        return percent_change
