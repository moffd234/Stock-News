import datetime

import requests
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()  # Finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found about

NEWS_KEY = os.getenv("NEWS_KEY")  # Gets the API Key
NEWS_URL = "https://newsapi.org/v2/everything"


def get_news(comp_name):
    today_date = str(datetime.date.today() - datetime.timedelta(days=1))
    yesterday_date = str(datetime.date.today() - datetime.timedelta(days=2))

    news_params = {
        "q": comp_name,
        "searchIn": "title",
        "from": yesterday_date,
        "to": today_date,
        "language": "en",
        "sortBy": "popularity",
        "pageSize": 3,  # The number of articles per page
        "apiKey": NEWS_KEY
    }
    news_request = requests.get(NEWS_URL, news_params)
    news_request.raise_for_status()
    return news_request.json()["articles"]  # Returns a dictionary of 3 articles
