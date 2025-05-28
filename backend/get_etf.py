from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--headless")  # GUI 끄기
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

def crawling(etf_code):
    try:
        # Toss 페이지 접속
        driver.get("https://tossinvest.com/")
        time.sleep(2)

        # 검색창 클릭 및 코드 입력
        search_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "u09klc0")))
        search_btn.click()

        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-section-name='검색']")))
        input_box.send_keys(etf_code)
        input_box.send_keys(Keys.ENTER)
        time.sleep(2)

        # 종목정보 탭 클릭
        info_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-contents-label='종목정보']")))
        info_tab.click()
        time.sleep(2)

        # 페이지 파싱
        soup = BeautifulSoup(driver.page_source, "html.parser")

        def get_text(selector):
            el = soup.select_one(selector)
            return el.text.strip() if el else "정보 없음"

        def find_value(label):
            items = soup.select("div._1ievn4p4")
            for item in items:
                if label in item.text:
                    val = item.select_one("p")
                    return val.text.strip() if val else "정보 없음"
            return "정보 없음"

        def find_stat(label):
            spans = soup.select("ul[data-list-name='Indicators'] li span.tw-wbeibam")
            for span in spans:
                if label in span.text:
                    val = span.find_parent().find_next_sibling("span")
                    return val.text.strip() if val else "정보 없음"
            return "정보 없음"

        # 주요 정보

        etf_name = get_text("div[data-section-name='ETF__회사정보'] h1 span:nth-of-type(1)")
        etf_ticker = get_text("div[data-section-name='ETF__회사정보'] h1 span:nth-of-type(2)")
        summary = get_text("div[data-section-name='ETF__회사정보'] div._1ievn4p6 span")

        nav = find_value("NAV")
        manager = find_value("운용사")
        marketcap = find_value("시가총액")
        asset = find_value("운용자산")
        issue = find_value("발행주식수")
        list_date = find_value("상장일")

        fee = find_stat("운용보수")
        gap = find_stat("괴리율")

        # 보유 종목 Top 10 (수정된 부분)
        holdings = []
        for block in soup.select("div._131kymtd"):
            spans = block.select("span")
            if len(spans) >= 2:
                name = spans[0].text.strip()
                weight = spans[1].text.strip()
                holdings.append((name, weight))

        # 배당 내역
        dividends = []
        for row in soup.select("div[data-section-name='ETF__배당금지급내역'] table tbody tr"):
            cols = row.select("td")
            if len(cols) >= 3:
                ex = cols[0].text.strip()
                pay = cols[1].text.strip()
                amt = cols[2].text.strip()
                dividends.append((ex, pay, amt))

        # 결과 출력
        print(f"\nETF 이름: {etf_name} ({etf_ticker})")
        print(f"운용사: {manager}")
        print(f"시가총액: {marketcap} / 운용자산: {asset}")
        print(f"NAV: {nav} / 상장일: {list_date}")
        print(f"운용보수: {fee} / 괴리율: {gap}")
        print(f"발행주식수: {issue}")
        print(f"\n 요약: {summary}")

        print("\n보유 종목 Top 10:")
        for name, weight in holdings:
            print(f"- {name}: {weight}")

        print("\n배당금 내역:")
        for ex, pay, amt in dividends:
            print(f"- 배당락일: {ex}, 지급일: {pay}, 주당: {amt}")

    finally:
        driver.quit()

# ✅ 실행
crawling("XLK")