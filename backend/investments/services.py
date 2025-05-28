import requests
from collections import defaultdict
import yfinance as yf
from datetime import datetime
from django.utils import timezone
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import lxml
import time

API_KEY = "2f6cdf934b056f7ae56c1bd479e2bfe6"


def get_rate_bounds(option_list):
    min_rate_map = defaultdict(lambda: float('inf'))
    max_rate_map = defaultdict(lambda: 0.0)

    for option in option_list:
        code = option['fin_prdt_cd']
        base = option.get('intr_rate')
        special = option.get('intr_rate2')

        if base is not None and base > 0:
            min_rate_map[code] = min(min_rate_map[code], base)

        if special is not None and special > 0:
            max_rate_map[code] = max(max_rate_map[code], special)

    return {
        code: (
            round(min_rate_map[code], 2) if min_rate_map[code] != float('inf') else None,
            round(max_rate_map[code], 2) if max_rate_map[code] > 0 else None
        )
        for code in set(min_rate_map) | set(max_rate_map)
    }


def get_interest_detail(option_list):
    detail_map = defaultdict(dict)
    for option in option_list:
        code = option['fin_prdt_cd']
        term = option.get('save_trm')
        if term:
            detail_map[code][term] = {
                'intr_rate': option.get('intr_rate'),
                'intr_rate2': option.get('intr_rate2')
            }
    return detail_map


def fetch_deposit_products():
    url = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"
    params = {'auth': API_KEY, 'topFinGrpNo': '020000', 'pageNo': '1'}

    res = requests.get(url, params=params)
    data = res.json()

    base_list = data['result']['baseList']
    option_list = data['result']['optionList']
    rate_bounds = get_rate_bounds(option_list)
    interest_detail = get_interest_detail(option_list)

    return base_list, rate_bounds, interest_detail


def fetch_savings_products():
    url = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
    params = {'auth': API_KEY, 'topFinGrpNo': '020000', 'pageNo': '1'}

    res = requests.get(url, params=params)
    data = res.json()

    base_list = data['result']['baseList']
    option_list = data['result']['optionList']
    rate_bounds = get_rate_bounds(option_list)
    interest_detail = get_interest_detail(option_list)

    return base_list, rate_bounds, interest_detail


def parse_datetime(value):
    try:
        dt = datetime.strptime(value, "%Y%m%d%H%M")
        return timezone.make_aware(dt)
    except Exception:
        return None


def parse_date(value):
    try:
        return datetime.strptime(value, "%Y%m%d").date()
    except Exception:
        return None


def fetch_etf_index_data(symbol, type_):
    # 한국 ETF인 경우 .KS 접미사 추가
    if not symbol.endswith(".KS") and not symbol.endswith(".KQ") and all(ord(c) < 128 for c in symbol):
        # 기본적으로 6자리 숫자라면 한국 ETF로 간주하고 .KS 붙이기
        if symbol.isdigit() and len(symbol) == 6:
            symbol += ".KS"

    ticker = yf.Ticker(symbol)
    info = ticker.info
    history = ticker.history(period="5d")

    results = []
    for i in range(len(history)):
        row = history.iloc[i]
        record_date = history.index[i].date()
        close_today = float(row["Close"])
        if i > 0:
            close_prev = float(history["Close"].iloc[i - 1])
            daily_change_pct = ((close_today - close_prev) / close_prev * 100) if close_prev != 0 else None
        else:
            daily_change_pct = None

        results.append({
            "symbol": symbol,
            "name": info.get("shortName", "N/A"),
            "data_type": type_,
            "record_date": record_date,
            "close_price": close_today,
            "daily_change_pct": daily_change_pct,
            "high_52w": info.get("fiftyTwoWeekHigh", None),
            "low_52w": info.get("fiftyTwoWeekLow", None),
            "aum": info.get("totalAssets", None) if type_ == "ETF" else None,
        })
    return results


def crawl_etf_detail(etf_code):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://tossinvest.com/")
        search_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "u09klc0")))
        search_btn.click()
        input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-section-name='검색']")))
        input_box.send_keys(etf_code)
        input_box.send_keys(Keys.ENTER)
        info_tab = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-contents-label='종목정보']")))
        info_tab.click()
        time.sleep(0.2)
        soup = BeautifulSoup(driver.page_source, "lxml")
        def get_text(selector):
            el = soup.select_one(selector)
            return el.text.strip() if el else None
        def find_value(label):
            items = soup.select("div._1ievn4p4")
            for item in items:
                if label in item.text:
                    val = item.select_one("p")
                    return val.text.strip() if val else None
            return None
        def find_stat(label):
            spans = soup.select("ul[data-list-name='Indicators'] li span.tw-wbeibam")
            for span in spans:
                if label in span.text:
                    val = span.find_parent().find_next_sibling("span")
                    return val.text.strip() if val else None
            return None
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
        holdings = []
        for block in soup.select("div._131kymtd"):
            spans = block.select("span")
            if len(spans) >= 2:
                name = spans[0].text.strip()
                weight = spans[1].text.strip()
                holdings.append({"name": name, "weight": weight})
        dividends = []
        for row in soup.select("div[data-section-name='ETF__배당금지급내역'] table tbody tr"):
            cols = row.select("td")
            if len(cols) >= 3:
                ex = cols[0].text.strip()
                pay = cols[1].text.strip()
                amt = cols[2].text.strip()
                dividends.append({"ex": ex, "pay": pay, "amt": amt})
        return {
            "code": etf_code,
            "name": etf_name,
            "ticker": etf_ticker,
            "manager": manager,
            "marketcap": marketcap,
            "asset": asset,
            "issue": issue,
            "list_date": list_date,
            "nav": nav,
            "fee": fee,
            "gap": gap,
            "summary": summary,
            "holdings": holdings,
            "dividends": dividends,
        }
    finally:
        driver.quit()
