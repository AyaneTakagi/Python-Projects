from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from time import sleep
import os
from dotenv import load_dotenv

"""
Tinder Auto Disliker - Tinder自動「イマイチ」プログラム

📌 プログラム概要 / Program Overview:
このプログラムはSeleniumを使用してTinderのログインとスワイプを自動化。
Facebookでのログイン、位置情報と通知の許可、GDPR同意画面の処理を行い、
無料枠（100回/日）の「Dislike（イマイチ）」を自動で実行。

This program automates the login and swiping process on Tinder using Selenium.
It handles login via Facebook, allows location and notifications, processes
the GDPR consent page, and automatically performs up to 100 "Dislikes" per day.

📌 使用する機能 / Features:
1. Facebookを使用してTinderに自動ログイン / Automatically logs into Tinder via Facebook.
2. 位置情報と通知の許可 / Grants location and notification permissions.
3. GDPR同意画面の処理（手動操作あり）/ Handles GDPR consent page (requires manual input).
4. 「Dislike（イマイチ）」を100回自動で実行 / Automatically performs up to 100 "Dislikes".
5. 「It's a Match!」ポップアップが表示された場合は閉じる / Closes the "It's a Match!" popup if it appears.
"""

load_dotenv()

FACEBOOK_EMAIL = os.getenv("FACEBOOK_EMAIL")
FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")

# Chromeを起動 / Launch Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# Tinderを開く / Open Tinder homepage
driver.get("https://tinder.com/")

# 「ログイン」ボタンをクリック / Click the "Log in" button
sleep(2)
log_in_button = driver.find_element(By.LINK_TEXT, value="Log in")
log_in_button.click()

# Cookieのポップアップを拒否 / Reject cookie popup
sleep(2)
reject_button = driver.find_element(By.XPATH, value="//div[contains(text(), 'I decline')]")
reject_button.click()

# Facebookでログイン / Login with Facebook
sleep(2)
log_in_with_facebook_button = driver.find_element(By.XPATH, value="//div[contains(text(), 'Log in with Facebook')]")
log_in_with_facebook_button.click()

# Facebookのログインウィンドウに切り替え / Switch to the Facebook login window
base_window = driver.window_handles[0]
fb_login_window = driver.window_handles[1]
driver.switch_to.window(fb_login_window)
print(driver.title)

# 2個目のCookieのポップアップを拒否 / Reject second cookie popup
sleep(5)
reject_button_2 = driver.find_element(By.XPATH, value="//span[contains(text(), 'Decline optional cookies')]")
driver.execute_script("arguments[0].click();", reject_button_2)

# Facebookのログイン情報を入力
sleep(3)
email_input = driver.find_element(By.ID, value="email")
email_input.send_keys(FACEBOOK_EMAIL)
password_input = driver.find_element(By.ID, value="pass")
password_input.send_keys(FACEBOOK_PASSWORD)
password_input.send_keys(Keys.ENTER)

# GDPR同意画面の確認（手動操作が必要）/ Handle GDPR consent page
print("⚠️ GDPR同意画面が表示されました。手動で同意しCAPTCHAを解いてください")
print("⚠️ GDPR consent page is displayed. Please agree and solve the CAPTCHA manually.")
input("Press Enter when you have solved...")  # ユーザーが手動で操作するのを待つ / Wait for the user to manually proceed

# 元のTinderウィンドウに戻る / Switch back to the Tinder window
driver.switch_to.window(base_window)
print(driver.title)

# 位置情報の許可 / Allow location access
sleep(2)
location_allow_button = driver.find_element(By.XPATH, value='//*[@id="c-1579927019"]/div/div/div/div/div[3]/button[1]/div[2]/div[2]')
location_allow_button.click()

# 通知の許可 / Allow notifications
sleep(2)
notification_allow_button = driver.find_element(By.XPATH, value='//*[@id="c-1579927019"]/div/div/div/div/div[3]/button[2]/div[2]/div[2]')
notification_allow_button.click()

# 無料枠（100回/日）の「Dislike（イマイチ）」 / 100 dislikes: Tinder free tier only allows 100 "Likes" per day.
for n in range(100):
    sleep(1)
    try:
        print("called")
        dislike_button = driver.find_element(By.CLASS_NAME, value="gamepad-icon-wrapper")
        dislike_button.click()

    # 「It's a Match!」のポップアップがある場合 / Handle "It's a Match!" popup
    except ElementClickInterceptedException:
        try:
            match_popup = driver.find_element(By.CSS_SELECTOR, value=".itsAMatch a")
            match_popup.click() # ポップアップを閉じる / Close the popup
        except NoSuchElementException:
            sleep(2) # ボタンがまだ読み込まれていない場合、2秒待つ / Wait 2 seconds if the button has not loaded yet

# ブラウザを閉じる
driver.quit()
