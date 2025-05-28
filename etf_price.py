import yfinance as yf
import pandas as pd

def get_etf_price_table(ticker: str, period='1y', interval='1d'):
    if ticker.isdigit():
        ticker += ".KS"

    etf = yf.Ticker(ticker)
    df = etf.history(period=period, interval=interval)

    if df.empty:
        return pd.DataFrame({"오류": [f"{ticker}에 대한 데이터를 불러올 수 없습니다."]})

    df = df[['Close']].reset_index()
    df.columns = ['날짜', '종가']
    df['날짜'] = df['날짜'].dt.date
    return df

# 사용 예시
df = get_etf_price_table("069500")  # 한국 ETF: KODEX 200
print(df)
