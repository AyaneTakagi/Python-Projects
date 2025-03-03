import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

SHEETY_ENDPOINT = "https://api.sheety.co/bc6e296eaa951072158f9238f8950101/flightDeals/prices"

class DataManager:

    def __init__(self):
        self.city_data = {}
        self._username = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._username, self._password)

    def get_city_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.city_data = data["prices"]
        return self.city_data

    def update_city_data(self):
        for city in self.city_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{SHEETY_ENDPOINT}/{city['id']}", json=new_data, auth=self._authorization)
            print(response.text)
