import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# 📌 プログラム概要 / Program Overview:
# Pixe.la API を使用して水泳の記録を管理。
# This script uses the Pixe.la API to track swimming records.
#
# 📌 参照しているAPI / APIs Used:
# - Pixe.la API (アクティビティ記録 / Activity tracking): https://pixe.la/ja

USERNAME = "ayane1123"
TOKEN = os.getenv("TOKEN")
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users" # https://docs.pixe.la/entry/post-user
user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}
# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs" # https://docs.pixe.la/entry/post-graph
graph_config = {
    "id": GRAPH_ID,
    "name": "Swimming Graph",
    "unit": "minutes",
    "type": "int",
    "color": "sora",
}
headers = {
    "X-USER-TOKEN": TOKEN,
}
# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)

pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}" # https://docs.pixe.la/entry/post-pixel
today = datetime.now()
pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("How many minutes did you swim today? "),
}
response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
print(response.text)

update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}" #https://docs.pixe.la/entry/put-pixel
update_data = {
    "quantity": "70",
}
# response = requests.put(url=update_endpoint, json=update_data, headers=headers)
# print(response.text)

delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}" # https://docs.pixe.la/entry/delete-pixel
# response = requests.delete(url=delete_endpoint, headers=headers)
# print(response.text)