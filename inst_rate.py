import requests
import xml.etree.ElementTree as ET
from datetime import date, timedelta, datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def get_korean_interest_rate(api_key='HJBKWZETG3PZGYDHMMUH'):
    today = date.today()
    end_month = today.strftime('%Y%m')
    start_year = today.year - 1
    start_month = f"{start_year}{today.month:02d}"

    url = (
        f"https://ecos.bok.or.kr/api/StatisticSearch/{api_key}/xml/kr/1/100/"
        f"722Y001/M/{start_month}/{end_month}/0101000"
    )
    response = requests.get(url)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.text)

    data = []
    for row in root.findall('./row'):
        date_str = row.findtext('TIME')
        value = row.findtext('DATA_VALUE')
        data.append((datetime.strptime(date_str, "%Y%m"), float(value)))
    return data

def get_fed_funds_rate_last_year(api_key):
    end_date = date.today()
    start_date = end_date - timedelta(days=365)

    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id=DFEDTARU"
        f"&api_key={api_key}"
        f"&file_type=json"
        f"&observation_start={start_date}"
        f"&observation_end={end_date}"
    )

    response = requests.get(url)
    data = response.json()
    observations = data.get("observations", [])
    result = []
    for obs in observations:
        if obs["value"] != ".":
            result.append((datetime.strptime(obs["date"], "%Y-%m-%d"), float(obs["value"])))
    return result

# ✅ API 키 입력
ecos_key = "HJBKWZETG3PZGYDHMMUH"
fred_key = "5111057dd0897bf1953e1ec8fa197afb"

# ✅ 데이터 가져오기
kr_data = get_korean_interest_rate(ecos_key)
us_data = get_fed_funds_rate_last_year(fred_key)

# 보간 전 데이터 → pandas 시리즈로 변환
kr_series = pd.Series(dict(kr_data))
us_series = pd.Series(dict(us_data))

# 전체 날짜 범위 생성 (일 단위)
full_dates = pd.date_range(start=min(kr_series.index.min(), us_series.index.min()),
                           end=max(kr_series.index.max(), us_series.index.max()),
                           freq='D')

# reindex + ffill
kr_filled = kr_series.reindex(full_dates).ffill()
us_filled = us_series.reindex(full_dates).ffill()

# 다시 리스트로 변환 (matplotlib에서 zip 사용 위함)
kr_data_filled = list(zip(kr_filled.index, kr_filled.values))
us_data_filled = list(zip(us_filled.index, us_filled.values))

# ✅ 차트 그리기
plt.figure(figsize=(12, 6))
plt.plot(*zip(*kr_data_filled), label="한국 기준금리")
plt.plot(*zip(*us_data_filled), label="미국 기준금리")

plt.title("최근 1년간 한미 기준금리 비교")
plt.xlabel("날짜")
plt.ylabel("기준금리 (%)")
plt.legend()
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
