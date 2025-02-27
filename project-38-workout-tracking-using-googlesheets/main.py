import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# 📌 プログラム概要 / Program Overview:
# このプログラムは、ユーザーが行った運動を入力すると、Nutritionix APIを使ってその運動の消費カロリーや時間を取得し、
# Sheety APIを使ってGoogle Sheetsに記録する。
# This program takes user input about exercises, fetches details (calories burned, duration)
# using the Nutritionix API, and logs the data to Google Sheets using the Sheety API.

# 📌 参照しているAPI / APIs Used:
# - Nutritionix API: https://developer.nutritionix.com/
# - Sheety API (Google Sheetsと連携 / Connects with Google Sheets): https://sheety.co/

load_dotenv()
# .env ファイルの例 / Example .env file:
# NUTRITIONIX_APP_ID=your_app_id
# NUTRITIONIX_API_KEY=your_api_key
# SHEETY_USERNAME=your_username
# SHEETY_PASSWORD=your_password

GENDER = "female"
WEIGHT_KG = 48
HEIGHT_CM = 155
AGE = 22

NUTRITIONIX_APP_ID = os.getenv("NUTRITIONIX_APP_ID")
NUTRITIONIX_API_KEY = os.getenv("NUTRITIONIX_API_KEY")
SHEETY_USERNAME = os.getenv("SHEETY_USERNAME")
SHEETY_PASSWORD = os.getenv("SHEETY_PASSWORD")

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ") # 例: "swam for 1 hour" / Example: "swam for 1 hour"

nutritionix_headers = { # https://www.nutritionix.com/business/api
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "Content-Type": "application/json",
}

params = { # https://trackapi.nutritionix.com/docs/#/default/post_v2_natural_exercise
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

# Nutritionix APIにリクエストを送信し、運動データを取得 / Send request to Nutritionix API and get exercise data
nutritionix_response = requests.post(url=nutritionix_endpoint, json=params, headers=nutritionix_headers)
exercise_data = nutritionix_response.json()

sheety_endpoint = "https://api.sheety.co/bc6e296eaa951072158f9238f8950101/workoutTracking/workouts"

today = datetime.now().strftime("%Y/%m/%d")
current_time = datetime.now().strftime("%H:%M:%S")

# 取得した運動データをGoogle Sheetsに保存 / Save retrieved exercise data to Google Sheets
for exercise in exercise_data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today,
            "time": current_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"],
        }
    }

    # Sheety APIにリクエストを送信し、Google Sheetsにデータを追加 / Send request to Sheety API and add data to Google Sheets
    sheety_response = requests.post(url=sheety_endpoint, json=sheet_inputs, auth=(SHEETY_USERNAME, SHEETY_PASSWORD))
    sheety_response.raise_for_status()
    print(f"Saved to Google Sheets: {sheety_response.json()}")
