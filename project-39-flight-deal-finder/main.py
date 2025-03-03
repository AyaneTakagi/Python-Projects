import time
from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

"""
Flight Deal Finder - フライトお得情報通知プログラム

📌 プログラム概要 / Program Overview:
このプログラムは、Google Sheetsに保存された都市リストをもとに、指定した出発地からの最安フライトを検索し、
設定した最低価格より安いフライトが見つかった場合に Twilioを利用して WhatsAppで通知を送信する。
This program searches for the cheapest flights from a specified departure city based on a list of cities stored in Google Sheets.
If a flight is found below a predefined price threshold, it sends a WhatsApp notification using Twilio.

📌️ 使用する機能 / Features:
1. Google Sheets から都市データを取得し、IATA コードを更新。/ Fetch city data from Google Sheets and update IATA codes.
2. 出発地 (TYO: 東京) からのフライトを検索し、最安値を比較。/ Search for flights from the departure city (TYO: Tokyo) and compare the lowest prices.
3. 設定した最低価格より安いフライトが見つかった場合、WhatsApp に通知を送信。/ Send a WhatsApp notification if a cheaper flight is found.

📌 使用するモジュール / Modules Used:
- data_manager.py: Google Sheets のデータ取得・更新 / Handles Google Sheets data retrieval and updates.
- flight_search.py: フライト検索 (IATA コード取得 & 価格チェック) / Searches for flights (IATA code retrieval & price checks).
- flight_data.py: フライトデータの処理 (最安フライトの選定) / Processes flight data (finds the cheapest flight).
- notification_manager.py: Twilio API を使用した WhatsApp 通知 / Sends WhatsApp notifications using the Twilio API.

📌 参照しているAPI / APIs Used:
- Google Sheet Data Management: https://sheety.co/
- Amadeus Flight Search API: https://developers.amadeus.com/
- Amadeus Flight Offer Docs: https://developers.amadeus.com/self-service/category/flights/api-doc/flight-offers-search/api-reference
- Amadeus Search for Airport Codes by City name: https://developers.amadeus.com/self-service/category/destination-experiences/api-doc/city-search/api-reference
- Twilio API: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn

📌 環境変数 (.env) / Environment Variables:
- SHEETY_USERNAME=your_sheety_username
- SHEETY_PASSWORD=your_sheety_password
- AMADEUS_API_KEY=your_amadeus_api_key
- AMADEUS_SECRET=your_amadeus_secret
- TWILIO_ACCOUNT_SID=your_twilio_account_sid
- TWILIO_AUTH_TOKEN=your_twilio_auth_token
- TWILIO_WHATSAPP_TO=whatsapp:+your_whatsapp_number

"""

# ==================== Set up the Flight Search ====================
data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()
sheet_data = data_manager.get_city_data()

ORIGIN_CITY_IATA = "TYO"

# ==================== Update the Airport Codes in Google Sheet ====================
for city in sheet_data:
    if city["iataCode"] == "":
        city["iataCode"] = flight_search.get_city_iatacode(city["city"])
        time.sleep(2)

print(f"sheet_data:\n{sheet_data}")

data_manager.city_data = sheet_data
data_manager.update_city_data()

# ==================== Search for Flights ====================
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flight(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today,
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: {cheapest_flight.price}")
    time.sleep(2)

# ==================== Send WhatsApp Message ====================
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")

        notification_manager.send_whatsapp_message(
            message_body = f"Low price alert! Only ¥{cheapest_flight.price} to fly "
                           f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                           f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )