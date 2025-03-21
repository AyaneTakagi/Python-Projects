from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
from dotenv import load_dotenv

"""
LinkedIn Job Application Bot - LinkedIn求人自動保存プログラム

📌 プログラム概要 / Program Overview:
このプログラムはLinkedInでの求人検索を自動化。
指定した条件で求人を検索し、保存可能な求人を保存し、企業をフォロー。
This program automates job searching on LinkedIn by finding job listings
based on specified criteria, saving jobs, and following companies.

📌 使用する機能 / Features:
1. LinkedInに自動ログイン / Automatically logs into LinkedIn.
2. 求人検索ページを開き、指定した条件で検索 / Opens the job search page with specified criteria.
3. 求人を自動保存 / Automatically saves job listings.
4. 企業を自動フォロー / Automatically follows companies.
"""

load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Chrome起動 / Open Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# LinkedIn起動 / Open LinkedIn homepage
driver.get("https://www.linkedin.com/")

# Cookieのポップアップを拒否 / Reject cookie popup
time.sleep(2)
reject_button = driver.find_element(By.CSS_SELECTOR, value="button[action-type='DENY']")
reject_button.click()

# サインインボタンをクリック / Click the "Sign in" button
time.sleep(2)
sign_in_button = driver.find_element(By.LINK_TEXT, value="Sign in")
sign_in_button.click()

# メールアドレスとパスワードを入力して、Enterキーを押してログイン / Enter email and password, then press Enter to log in
time.sleep(3)
email_input = driver.find_element(By.ID, value="username")
email_input.send_keys(LINKEDIN_EMAIL)
password_input = driver.find_element(By.ID, value="password")
password_input.send_keys(LINKEDIN_PASSWORD)
password_input.send_keys(Keys.ENTER)

# CAPTCHA対応待ち / Wait for the user to manually solve the CAPTCHA before proceeding
print("⚠️ Solve the CAPTCHA manually and then press Enter.")
input("Press Enter when you have solved the CAPTCHA")

# 求人検索ページ起動 / Open the job search page with specific criteria
time.sleep(5)
driver.get("https://www.linkedin.com/jobs/search/"
           "?currentJobId=4166308729&distance=25&f_AL=true&f_E=1&geoId=106079947"
           "&keywords=software%20developer%20intern&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true")

# 求人リスト取得 / Retrieve job listings
time.sleep(3)
all_listings = driver.find_elements(By.CSS_SELECTOR, value="div.job-card-container--clickable")

# 求人を保存 & 企業をフォロー / Save each job and follow the company
for listing in all_listings:
    print("Opening Listing")
    driver.execute_script("arguments[0].click();", listing)
    time.sleep(2)

    try:
        # 求人を保存 / Click Save Button
        job_save_button = driver.find_element(By.CLASS_NAME, value="jobs-save-button")
        job_save_button.click()

        # 企業のフォローボタンをクリック / Click the Follow button for the company
        time.sleep(2)
        company_follow_button = driver.find_element(By.CLASS_NAME, value="follow")
        about_the_company = driver.find_element(By.CSS_SELECTOR, value=".jobs-company__box")
        driver.execute_script("arguments[0].scrollIntoView();", about_the_company)
        time.sleep(1)
        company_follow_button.click()
        time.sleep(2)

    except NoSuchElementException:
        print("No application button, skipped.")

time.sleep(5)
driver.quit()
print("✅ Job saved & company followed!")