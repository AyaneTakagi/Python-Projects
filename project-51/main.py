from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
from dotenv import load_dotenv

"""
Internet Speed Twitter Bot - インターネット速度を自動で計測し、プロバイダーにツイートするボット

📌 プログラム概要 / Program Overview:
このプログラムは、Seleniumを使用してインターネットの速度を計測し、指定した速度が契約内容に合っていない場合にTwitterにツイートする。
Speedtest.netを使用して速度を測定し、速度測定後にプロバイダーに対して自動でツイートを送信。

This program automates the process of measuring internet speed using Selenium and tweets at the internet provider if the speed does not match the promised speeds.
It uses Speedtest.net to measure the internet speed and automatically sends a tweet to the provider after the test.

📌 使用する機能 / Features:
1. Speedtest.netを使用してインターネット速度を計測 / Measures internet speed using Speedtest.net.
2. ダウンロードとアップロード速度を取得 / Retrieves download and upload speeds.
3. 契約されたインターネット速度と比較し、ツイートの内容を生成 / Compares the speed with the promised speed and generates the tweet.
4. Twitter（X.com）に自動でログイン / Automatically logs into Twitter (X.com).
5. 速度が契約内容に合っていない場合、プロバイダーにツイートを送信 / Sends a tweet to the provider if the speed does not match the promised speed.
6. クッキーの同意、ログイン処理などの手順を自動化 / Automates cookie consent, login, and other necessary steps.

📌 環境変数 (.env) / Environment Variables:
- TWITTER_USERNAME=your_twitter_username
- TWITTER_EMAIL=your_twitter_email_address
- TWITTER_PASSWORD=your_twitter_password
"""

load_dotenv()

PROMISED_DOWN=150
PROMISED_UP=10
TWITTER_USERNAME=os.getenv("TWITTER_USERNAME")
TWITTER_EMAIL=os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD=os.getenv("TWITTER_PASSWORD")


class InternetSpeedTwitterBot:

    def __init__(self):
        self.driver = webdriver.Chrome() # WebDriverの初期化 / Initialize the WebDriver
        self.down = 0 # ダウンロード速度 (Download speed)
        self.up = 0 # アップロード速度 (Upload speed)

    def get_internet_speed(self):

        # speedtestを開く / Open speedtest
        self.driver.get("https://www.speedtest.net/")

        # クッキーを拒否 / Reject cookies
        sleep(2)
        cookie_reject_button = self.driver.find_element(By.ID, value="onetrust-reject-all-handler")
        cookie_reject_button.click()

        # 「GO」ボタンをクリック / Click the "GO" button
        sleep(2)
        go_button = self.driver.find_element(By.CLASS_NAME, value="start-text")
        go_button.click()

        sleep(90) # スピードテストが終了するまで待機 / Wait for the speed test to finish

        # "Speedtest for Mac" ボタンをクリック / Click the "Speedtest for Mac" button
        try_speedtest_for_mac_button = self.driver.find_element(By.XPATH, value='//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/div[1]/div[3]/div/div[8]/div/div/div[2]/a')
        try_speedtest_for_mac_button.click()

        # ダウンロードとアップロードの速度を取得 / Get the download and upload speeds
        self.down = self.driver.find_element(By.CLASS_NAME, value="download-speed").text
        self.up = self.driver.find_element(By.CLASS_NAME, value="upload-speed").text

        print(f"Download Speed: {self.down} Mbps")
        print(f"Upload Speed: {self.up} Mbps")

    def tweet_at_provider(self):

        # Twitterを開く / Open Twitter
        self.driver.get("https://x.com/")

        # クッキーを拒否 / Reject cookies
        sleep(2)
        cookie_reject_button2 = self.driver.find_element(By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div[2]/button[2]/div')
        cookie_reject_button2.click()

        # サインインボタンをクリック / Click the sign-in button
        sleep(2)
        sign_in_button = self.driver.find_element(By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[3]/a/div')
        sign_in_button.click()

        # ユーザー名を入力 / Enter the username
        sleep(3)
        username_input = self.driver.find_element(By.NAME, "text")
        username_input.send_keys(TWITTER_USERNAME)
        username_input.send_keys(Keys.ENTER)

        # メールアドレスを入力 (もし要求される場合) / Enter the email (if requested)
        sleep(3)
        email_input_elements = self.driver.find_elements(By.NAME, "text")
        if len(email_input_elements) > 0:
            email_input = email_input_elements[0]
            email_input.send_keys(TWITTER_EMAIL)
            email_input.send_keys(Keys.ENTER)

        # パスワードを入力 / Enter the password
        sleep(3)
        password_input = self.driver.find_element(By.NAME, "password")
        password_input.send_keys(TWITTER_PASSWORD)
        password_input.send_keys(Keys.ENTER)

        # ツイートを作成 / Compose the tweet
        sleep(3)
        tweet_input = self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
        tweet = f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_input.send_keys(tweet)

        # ツイートを投稿するボタンをクリック / Click the post tweet button
        sleep(2)
        post_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button')
        post_button.click()

        # ブラウザを閉じる / Close the browser
        sleep(2)
        self.driver.quit()


bot = InternetSpeedTwitterBot() # インスタンスを作成して実行 / Create an instance and run
bot.get_internet_speed() # インターネットの速度を取得 / Get internet speed
bot.tweet_at_provider() # インターネットプロバイダーにツイート / Tweet at the internet provider