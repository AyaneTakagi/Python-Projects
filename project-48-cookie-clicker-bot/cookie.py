from selenium import webdriver
from selenium.webdriver.common.by import By
import time

"""
Cookie Clicker Bot using Selenium - クッキークリッカー自動化プログラム

📌 プログラム概要 / Program Overview:
このプログラムはCookie Clickerのゲームを自動化。
一定時間ごとにクッキーをクリックし購入可能なアップグレードがあれば自動的に購入。
This program automates the Cookie Clicker game by clicking the cookie periodically
and purchasing available upgrades when affordable.

📌 使用する機能 / Features:
1. クッキーを自動でクリック / Automatically clicks the cookie.
2. 購入可能なアップグレードを自動購入 / Automatically buys the most expensive affordable upgrade.
3. 5分後にクッキーの生成速度 (CPS) を表示 / Displays cookies per second (CPS) after 5 minutes.
"""

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Get cookie to click on.
cookie = driver.find_element(By.ID, value="cookie")

timeout = time.time() + 5
five_min = time.time() + 60*5  # 5 minutes

while True: # stop in 5 minutes
    cookie.click()

    # Every 5 seconds:
    if time.time() >= timeout:

        # Get current cookie count
        money = driver.find_element(By.ID, value="money").text
        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)

        # Find upgrades that we can currently afford
        upgrades = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        affordable_upgrades_dict = {}
        for upgrade in upgrades:
            if "-" in upgrade.text:
                name = upgrade.text.split("-")[0].strip()
                price = int(upgrade.text.split("-")[1].strip().replace(",", ""))
                affordable_upgrades_dict[name] = price
        affordable_upgrades = {name: price for name, price in affordable_upgrades_dict.items() if price <= cookie_count}

        # Purchase the most expensive affordable upgrade
        if affordable_upgrades:
            highest_price_affordable_upgrade = max(affordable_upgrades, key=affordable_upgrades.get)
            print(highest_price_affordable_upgrade)
            driver.find_element(By.ID, value=f"buy{highest_price_affordable_upgrade}").click()
        else:
            print("No affordable upgrades available.")

        # Add another 5 seconds until the next check
        timeout = time.time() + 5

    # After 5 minutes, stop the bot and check the cookies per second count.
    if time.time() >= five_min:
        cookie_per_second = driver.find_element(by=By.ID, value="cps").text
        print(cookie_per_second)
        break
