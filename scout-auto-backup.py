from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import re

load_dotenv()

email = os.getenv("INFRA_EMAIL")
password = os.getenv("INFRA_PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=False)
    page = browser.new_page()

    # ログイン
    page.goto("https://enterprise.in-fra.jp/login")
    page.fill("#name", email)
    page.fill("#password", password)
    page.click("//button[@type='button']")
    page.wait_for_load_state("networkidle")
    print("login ok")

    # スカウトページへ
    page.goto("https://enterprise.in-fra.jp/scouts")
    page.wait_for_load_state("networkidle")
    print("scout ok")

    # 保存済み検索条件 → 関西
    page.get_by_text("保存済みの検索条件").click()
    page.wait_for_timeout(1000)
    search_btn = page.locator("input#standard-adornment-name-1 ~ button:has-text('検索')").first
    search_btn.click()
    page.wait_for_load_state("networkidle")
    print("kansai ok")

    # 学生カード取得
    student_cards = page.locator("div.css-1i369cv").all()
    print(f"学生数: {len(student_cards)}人")

    qualified = []

    for card in student_cards:
        # 大学名
        try:
            univ_text = card.locator(".e12i0ovq3").first.inner_text()
        except:
            univ_text = "不明"

        # 稼働時間
        hours = ""
        try:
            spans = card.locator("p.e12i0ovq2 span.value").all()
            for span in spans:
                t = span.inner_text()
                if "時間" in t:
                    hours = t
                    break
        except:
            pass

        # スコアリング
        is_qualified = False
        if hours:
            nums = re.findall(r'\d+', hours)
            if nums and int(nums[0]) >= 32:
                is_qualified = True

        if is_qualified:
            qualified.append({"大学": univ_text, "稼働": hours})
            print(f"✅ {univ_text} | {hours}")
        else:
            print(f"❌ {univ_text} | {hours}")

    print(f"\n条件クリア: {len(qualified)}人 / {len(student_cards)}人")

    input("press enter...")
    browser.close()
    