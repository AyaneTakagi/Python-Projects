import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# 📌 プログラム概要 / Program Overview:
# このプログラムは、Tesla (TSLA) の株価変動を監視し、変動率が3%以上の場合に関連ニュースを取得。
# そのニュースをTwilioを使ってWhatsAppに送信する。
# This program monitors the stock price changes of Tesla (TSLA).
# If the price change exceeds 3%, it fetches related news and sends it via WhatsApp using Twilio.

# 📌 参照しているAPI / APIs Used:
# - Alpha Vantage API (株価データ取得 / Fetching stock data): https://www.alphavantage.co/documentation/
# - NewsAPI (ニュース取得 / Fetching news articles): https://newsapi.org/docs/endpoints/everything
# - Twilio API (WhatsApp メッセージ送信 / Sending WhatsApp messages): https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.getenv("STOCK_API_KEY") # https://www.alphavantage.co/support/#api-key
NEWS_API_KEY = os.getenv("NEWS_API_KEY") # https://newsapi.org/
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_TO = os.getenv("TWILIO_WHATSAPP_TO")

stock_params = { # https://www.alphavantage.co/documentation/#daily
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

# 昨日の終値 / Yesterday's closing price
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# 一昨日の終値 / Day before yesterday's closing price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# 株価変動の計算 / Calculate price difference
price_difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = "🔺" if price_difference > 0 else "🔻"

percentage_difference = round((price_difference / float(yesterday_closing_price)) * 100)

# 株価変動が3%以上ならニュースを取得 / Fetch news if stock price change is greater than 1%
if abs(percentage_difference) > 3:
    news_params = { # https://newsapi.org/docs/endpoints/everything
        "apiKey": NEWS_API_KEY,
        "q": COMPANY_NAME,
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    formatted_articles = [
        (f"{STOCK_NAME}: {up_down}{percentage_difference}%\n"
         f"Headline: {article['title']}.\n"
         f"Brief: {article['description']}\n"
         f"URL: {article['url']}") for article in three_articles
    ]

    # Twilioを使ってWhatsAppメッセージを送信 / Send WhatsApp messages using Twilio
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=article,
            to=TWILIO_WHATSAPP_TO,
        )
        print(message.sid)