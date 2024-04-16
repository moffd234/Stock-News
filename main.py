import os
import news
from twilio.rest import Client
from stockInfo import StockInfo
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()  # Finds the .env file path
load_dotenv(dotenv_path)  # loads the .env file from the path found about
PHONE_NUMBER = os.getenv("PHONE_NUMBER")
TWILIO_AUTH = os.getenv("auth_token")
TWILIO_SID = os.getenv("account_sid")
USER_PHONE_NUMBER = os.getenv("USER_PHONE_NUMBER_NEWS")
twilio_client = Client(TWILIO_SID, TWILIO_AUTH)

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_data = StockInfo(STOCK)
percent_changed = stock_data.find_change()

if abs(percent_changed) >= 5:
    articles = news.get_news(STOCK)
    print(len(articles))
    for line in articles:
        if percent_changed > 0:
            message = twilio_client.messages.create(
                from_=PHONE_NUMBER,
                body=f"{STOCK}: 🔺{round(percent_changed, 2)}% \n\nTitle: {line['title']}\n\nBrief: "
                     f"{line['description']}",
                to=USER_PHONE_NUMBER
            )
            print(message.status)
        else:
            message = twilio_client.messages.create(
                from_=PHONE_NUMBER,
                body=f"{STOCK}: 🔻{round(percent_changed, 2)}% Title: {line['title']}\n\nBrief: {line['description']}",
                to=USER_PHONE_NUMBER
            )
            print(message.status)


"""TSLA: 🔺2% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey have 
gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings 
show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash. 

or
 
"TSLA: 🔻5% Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. Brief: We at Insider Monkey 
have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F 
filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus 
market crash."""

