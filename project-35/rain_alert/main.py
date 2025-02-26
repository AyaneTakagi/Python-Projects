import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv


load_dotenv()

# 📌 参照しているAPI / APIs Used:
# - OpenWeatherMap API: https://openweathermap.org/forecast5
# - Twilio API (WhatsApp メッセージ送信 / Sending WhatsApp messages): https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

# OpenWeatherMap APIのエンドポイントとキー / OpenWeatherMap API endpoint and key
OpenWeatherMap_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
OpenWeatherMap_api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")

# Twilio APIの認証情報 / Twilio API authentication
Twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
Twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

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
if will_rain:
    client = Client(Twilio_account_sid, Twilio_auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="It's going to rain today. Remember to bring an ☔️",
        to='whatsapp:+818028701123'
    )
    print(message.sid)
else:
    client = Client(Twilio_account_sid, Twilio_auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="It's a nice sunny day ☀️",
        to='whatsapp:+818028701123'
    )
    print(message.sid)
