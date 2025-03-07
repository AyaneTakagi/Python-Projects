from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

"""
Amazon Price Checker - 商品の価格をAmazonから取得し、設定した価格より安くなった場合にメールを送信するプログラム

📌 プログラム概要 / Program Overview:
このプログラムは、指定したAmazonの商品ページから価格情報を取得し、価格が設定した値段より低い場合メールを送信する。
This program fetches price information from a specified Amazon product page and emails if the price is below the set value.

📌 使用する機能 / Features:
1. 商品ページのURLを指定して価格を取得 / Provide the product page URL and fetch the price.
2. 価格情報を抽出して表示 / Extract the price and display it.
3. 価格が設定した閾値より低くなった場合、通知メールを送信 / Send a notification email if the price is below the threshold.

📌 環境変数 (.env) / Environment Variables:
- SMTP_ADDRESS="smtp.gmail.com"
- EMAIL_ADDRESS=your_email_address
- EMAIL_PASSWORD=your_app_password
"""

SMTP_ADDRESS = os.environ["SMTP_ADDRESS"]
EMAIL_ADDRESS = os.environ["EMAIL_ADDRESS"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

url = "https://www.amazon.co.jp/-/en/dp/B07FD2FPMC/ref=sr_1_2?crid=HPJGJQ5T8PDS&dib=eyJ2IjoiMSJ9.HCBJRH8TvswaBPVBRHG-MLq6MsaPm_hC2X-tleIvqSv7yOZW1T0A7UGUt0oQAlIhm1U1JRyEXAlRZ4bolDnb7yADXh3ehmrJkeqiAXKfjAhWBdoPEdUgezon57Q2z9UKUi4skMJhNK5EDmXFVyHciGVL2wCskOeXpO0etkCPakm5aJwgwXguejWr1SY3FRG7pMvzVvbUVcCXxmWvQVLcGquyXp6g8B2TeVzyUA3PZpw.sP3ueGM-j6as3H4tMza-RYsqiavdRS7NVEWTCkfVaMo&dib_tag=se&keywords=%E3%82%B9%E3%83%9E%E3%83%96%E3%83%A9&qid=1741374989&s=videogames&sprefix=suma%2Cvideogames%2C529&sr=1-2&th=1"

headers = {
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

response = requests.get(url=url, headers=headers)
website = response.content
soup = BeautifulSoup(website, "html.parser")
# print(soup.prettify())

price = int("".join(soup.find(name="span", class_="a-price-whole").getText().split(",")))
print(price)

product_title = " ".join(soup.find(name="span", id="productTitle").getText().split())
print(product_title)

# この価格以下になったときに通知を受け取るための値段設定 / Set the price below which you would like to get a notification
BUY_PRICE = 7000

if price < BUY_PRICE:
    message = f"{product_title} is now ¥{price}!"

    with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
        connection.starttls()
        connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        connection.sendmail(
            from_addr=EMAIL_ADDRESS,
            to_addrs=EMAIL_ADDRESS,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
        )

    print("Email sent successfully!")