from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import re

load_dotenv()

email = os.getenv("INFRA_EMAIL")
password = os.getenv("INFRA_PASSWORD")

priority_universities = [
    "東京大学", "京都大学", "大阪大学", "東北大学", "名古屋大学", "九州大学", "北海道大学",
    "早稲田大学", "慶應義塾大学",
    "関西学院大学", "関西大学", "同志社大学", "立命館大学"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://enterprise.in-fra.jp/login")
    page.wait_for_timeout(2000)
    page.fill("#name", email)
    page.fill("#password", password)
    page.click("button[type='button']")
    page.wait_for_timeout(3000)
    print("login ok")

    page.goto("https://enterprise.in-fra.jp/scouts")
    page.wait_for_timeout(3000)
    print("scout ok")

    try:
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
    except:
        pass

    page.click("button:has-text('保存済みの検索条件')")
    page.wait_for_timeout(2000)

    # standard-adornment-name-0の次の兄弟要素のボタンをクリック
    page.evaluate("""
        const input = document.getElementById('standard-adornment-name-0');
        const parent = input.closest('div').parentElement.parentElement;
        const btn = parent.querySelector('button.MuiButton-sizeSmall');
        if (btn) btn.click();
    """)
    page.wait_for_timeout(3000)
    print("kansai ok")

    cards = page.locator("div.css-1i369cv").all()
    print(f"学生数: {len(cards)}人")

    qualified = []

    for card in cards:
        try:
            univ_text = card.locator("div.e12i0ovq3").inner_text()
        except:
            univ_text = "不明"

        try:
            spans = card.locator("p.e12i0ovq2 span.value").all()
            hours = ""
            for span in spans:
                text = span.inner_text()
                if "時間" in text:
                    hours = text
                    break
        except:
            hours = ""

        is_qualified = False
        if hours:
            nums = re.findall(r'\d+', hours)
            if nums and int(nums[0]) >= 32:
                is_qualified = True

        is_priority = any(u in univ_text for u in priority_universities)

        if is_qualified:
            if is_priority:
                print(f"⭐ {univ_text} | {hours}")
                qualified.append({"大学": univ_text, "稼働": hours, "優先度": "高"})
            else:
                print(f"✅ {univ_text} | {hours}")
                qualified.append({"大学": univ_text, "稼働": hours, "優先度": "低"})
        else:
            print(f"❌ {univ_text} | {hours}")

    print(f"\n条件クリア: {len(qualified)}人")
    print(f"⭐優先: {len([q for q in qualified if q['優先度'] == '高'])}人")

    input("press enter...")
    browser.close()