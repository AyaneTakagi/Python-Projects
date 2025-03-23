import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

"""
Google Form Auto-Filler Bot - Googleフォームに自動でデータを入力するボット

📌 プログラム概要 / Program Overview:
このプログラムは、指定したURLのWebページから賃貸物件の情報（リンク、住所、価格）を取得し、その情報をGoogleフォームに自動で入力して送信。
BeautifulSoupを使用してWebページを解析し、Seleniumを使用してGoogleフォームにデータを入力する。

This program scrapes rental property information (links, addresses, and prices) from a specified URL and automatically fills out a Google Form with the data.
It uses BeautifulSoup to parse the webpage and Selenium to input data into the Google Form.

📌 使用する機能 / Features:
1. 指定されたWebページから賃貸物件情報を取得 / Scrapes rental property information from a specified webpage.
2. WebページのHTMLを解析するためにBeautifulSoupを使用 / Uses BeautifulSoup to parse the webpage's HTML.
3. リンク、住所、価格を抽出 / Extracts links, addresses, and prices.
4. Googleフォームに自動でデータを入力 / Automatically inputs data into the Google Form.
5. Googleフォームにデータを入力するためにSeleniumを使用 / Uses Selenium to input data into the Google Form.
6. 入力後、フォームを送信 / Submits the form after inputting the data.
7. フォーム送信後、再度フォームをリセット / Resets the form after submission.

"""

# 賃貸物件のリンク、住所、価格を取得 / Scrape the links, addresses, and prices of the rental properties
zillow_clone_url = "https://appbrewery.github.io/Zillow-Clone/" # Use the Zillow-Clone website (instead of Zillow.com)
google_form_url = "https://docs.google.com/forms/d/e/1FAIpQLScDw2FsvDoPTeJoeDyBo0zJQlPYLZmkMe_WAvoe3wuf9_WeiQ/viewform"

# ヘッダーの設定 / Set headers for the HTTP request
headers = { # 言語設定とブラウザのユーザーエージェント / Language setting and browser user-agent
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

# Zillow-Cloneのページからデータを取得 / Fetch data from the Zillow-Clone page
response = requests.get(url=zillow_clone_url, headers=headers)
website = response.text

# BeautifulSoupでHTMLを解析 / Parse the HTML using BeautifulSoup
soup = BeautifulSoup(website, "html.parser")

# リンクを取得 / Extract all links
all_links = soup.find_all(name="a", class_="property-card-link")
link_list = [link.get("href") for link in all_links]
print(link_list)

# 価格を取得 / Extract prices
all_prices = soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
price_list = [price.getText().split("+")[0].split("/")[0] for price in all_prices]
print(price_list)

# 住所を取得 / Extract addresses
all_addresses = soup.find_all(name="address", attrs={"data-test": "property-card-addr"})
address_list = [address.getText().split("|")[-1].strip() for address in all_addresses]
print(address_list)

# Googleフォームにデータを入力 / Fill in the Google Form using Selenium
# Chromeを起動 / Launch Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# google formを開く / Open google form
driver.get(google_form_url)

sleep(2)

# 取得したデータをフォームに入力 / Input the extracted data into the form
for i in range(len(link_list)):
    each_link = link_list[i]
    each_price = price_list[i]
    each_address = address_list[i]

    sleep(2)
    # 各フィールドにデータを入力 / Input data into each field
    link_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    # 各入力フィールドにデータを送信 / Send data to each input field
    link_input.send_keys(each_link)
    price_input.send_keys(each_price)
    address_input.send_keys(each_address)

    # 送信ボタンをクリック / Click the submit button
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    submit_button.click()

    # フォーム送信後、フォームをリセットして再利用可能に / Reset the form after submission for reuse
    sleep(2)
    driver.get(google_form_url)
    sleep(1)

# 終了 / Close the browser
driver.quit()
