from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from dotenv import load_dotenv
import os
import time
import re

load_dotenv()

email = os.getenv("INFRA_EMAIL")
password = os.getenv("INFRA_PASSWORD")

priority_universities = [
    "東京大学", "京都大学", "大阪大学", "東北大学", "名古屋大学", "九州大学", "北海道大学",
    "早稲田大学", "慶應義塾大学",
    "関西学院大学", "関西大学", "同志社大学", "立命館大学"
]

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
wait = WebDriverWait(driver, 10)

driver.get("https://enterprise.in-fra.jp/login")
time.sleep(2)

email_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
email_field.send_keys(email)

password_field = driver.find_element(By.ID, "password")
password_field.send_keys(password)

login_button = driver.find_element(By.XPATH, "//button[@type='button']")
login_button.click()
time.sleep(3)

print("login ok")

driver.get("https://enterprise.in-fra.jp/scouts")
time.sleep(3)

print("scout ok")

saved_search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '保存済みの検索条件')]")))
saved_search_button.click()
time.sleep(2)

kansai_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='standard-adornment-name-0']/following::button[contains(text(), '検索')]")))
driver.execute_script("arguments[0].click();", kansai_button)
time.sleep(3)

print("kansai ok")

student_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'css-1i369cv')]")
print(f"学生数: {len(student_cards)}人")

qualified = []

for i, card in enumerate(student_cards):
    try:
        univ = card.find_element(By.XPATH, ".//div[contains(@class, 'e12i0ovq3')]")
        univ_text = univ.text
    except:
        univ_text = "不明"

    try:
        work_info = card.find_elements(By.XPATH, ".//p[contains(@class, 'e12i0ovq2')]//span[@class='value']")
        hours = ""
        for w in work_info:
            if "時間" in w.text:
                hours = w.text
    except:
        hours = ""

    is_qualified = False
    if hours:
        nums = re.findall(r'\d+', hours)
        if nums:
            h_num = int(nums[0])
            if h_num >= 32:
                is_qualified = True

    is_priority = any(univ in univ_text for univ in priority_universities)

    if is_qualified:
        if is_priority:
            qualified.append({"大学": univ_text, "稼働": hours, "優先度": "高"})
            print(f"⭐ {univ_text} | {hours}")
        else:
            qualified.append({"大学": univ_text, "稼働": hours, "優先度": "低"})
            print(f"✅ {univ_text} | {hours}")
    else:
        print(f"❌ {univ_text} | {hours}")

print(f"\n条件クリア: {len(qualified)}人 / {len(student_cards)}人")
print(f"⭐優先: {len([q for q in qualified if q['優先度'] == '高'])}人")
print(f"✅通常: {len([q for q in qualified if q['優先度'] == '低'])}人")

input("press enter...")
driver.quit()