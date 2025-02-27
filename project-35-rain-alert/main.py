import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

# 📌 プログラム概要 / Program Overview:
# このプログラムは天気予報を取得し、雨が降る場合はTwilioを使ってWhatsAppに送信する。
# This program fetches the weather forecast and sends a WhatsApp notification using Twilio if it will rain.

# 📌 参照しているAPI / APIs Used:
# - OpenWeatherMap API: https://openweathermap.org/forecast5
# - Twilio API (WhatsApp メッセージ送信 / Sending WhatsApp messages): https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

load_dotenv()
# 📌 .env ファイルの例 / Example .env file:
# OPEN_WEATHER_MAP_API_KEY=your_open_weather_map_api_key
# TWILIO_ACCOUNT_SID=your_twilio_account_sid
# TWILIO_AUTH_TOKEN=your_twilio_auth_token
# TWILIO_WHATSAPP_TO=whatsapp:+your_whatsapp_number

# OpenWeatherMap APIのエンドポイントとキー / OpenWeatherMap API endpoint and key
OpenWeatherMap_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
OpenWeatherMap_api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

# Twilio APIの認証情報 / Twilio API authentication
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_TO = os.getenv("TWILIO_WHATSAPP_TO")

weather_params = {
    "lat": 47.533340,
    "lon": 21.625210,
    "appid": OpenWeatherMap_api_key,
    "cnt": 4,
}

response = requests.get(url=OpenWeatherMap_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

# 雨が降るかどうか判定 / Check if it will rain
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700: # 700未満は雨や雪などの天候 / Codes below 700 indicate rain or snow
        will_rain = True

# Twilioを使ってWhatsAppメッセージを送信 / Send WhatsApp message using Twilio
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
if will_rain:
    message_body = "It's going to rain today. Remember to bring an ☔️"
else:
    message_body = "It's a nice sunny day ☀️"
message = client.messages.create(
    from_='whatsapp:+14155238886', # Twilioの公式WhatsApp送信番号 / Twilio's WhatsApp number
    body=message_body,
    to=TWILIO_WHATSAPP_TO,
)
print(message.sid)
