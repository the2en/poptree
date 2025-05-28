from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import InvestmentProduct, DailyMarketData
from .services import fetch_deposit_products, fetch_savings_products, fetch_etf_index_data
from investments.services import parse_date, parse_datetime
from django.db.models import Q
import requests
import xml.etree.ElementTree as ET
from datetime import date, timedelta, datetime
import yfinance as yf


@api_view(['GET'])
def fetch_and_store_deposit_products(request):
    base_list, rate_bounds, interest_detail = fetch_deposit_products()
    saved_count = 0

    for item in base_list:
        code = item['fin_prdt_cd']
        lowest, highest = rate_bounds.get(code, (None, None))

        _, created = InvestmentProduct.objects.update_or_create(
            fin_prdt_cd=code,
            defaults={
                'fin_co_no': item['fin_co_no'],
                'kor_co_nm': item['kor_co_nm'],
                'fin_prdt_nm': item['fin_prdt_nm'],
                'type': '예금',
                'join_way': item.get('join_way'),
                'join_deny': item.get('join_deny'),
                'join_member': item.get('join_member'),
                'spcl_cnd': item.get('spcl_cnd'),
                'etc_note': item.get('etc_note'),
                'mtrt_int': item.get('mtrt_int'),
                'intr_rate_type_nm': item.get('intr_rate_type_nm'),
                'max_limit': item.get('max_limit'),
                'interest_detail': interest_detail.get(code, {}),
                'lowest_rate': lowest,
                'highest_rate': highest,
                'dcls_month': item['dcls_month'],
                'dcls_strt_day': parse_date(item['dcls_strt_day']),
                'dcls_end_day': parse_date(item.get('dcls_end_day')),
                'fin_co_subm_day': parse_datetime(item['fin_co_subm_day']),

            }
        )
        if created:
            saved_count += 1

    queryset = InvestmentProduct.objects.filter(type='예금').values()
    return Response({
        "message": f"{saved_count}개 저장됨",
        "products": list(queryset)
    })


@api_view(['GET'])
def fetch_and_store_savings_products(request):
    base_list, rate_bounds, interest_detail = fetch_savings_products()
    saved_count = 0

    for item in base_list:
        code = item['fin_prdt_cd']
        lowest, highest = rate_bounds.get(code, (None, None))

        _, created = InvestmentProduct.objects.update_or_create(
            fin_prdt_cd=code,
            defaults={
                'fin_co_no': item['fin_co_no'],
                'kor_co_nm': item['kor_co_nm'],
                'fin_prdt_nm': item['fin_prdt_nm'],
                'type': '적금',
                'join_way': item.get('join_way'),
                'join_deny': item.get('join_deny'),
                'join_member': item.get('join_member'),
                'spcl_cnd': item.get('spcl_cnd'),
                'etc_note': item.get('etc_note'),
                'mtrt_int': item.get('mtrt_int'),
                'intr_rate_type_nm': item.get('intr_rate_type_nm'),
                'max_limit': item.get('max_limit'),
                'interest_detail': interest_detail.get(code, {}),
                'lowest_rate': lowest,
                'highest_rate': highest,
                'dcls_month': item['dcls_month'],
                'dcls_strt_day': parse_date(item['dcls_strt_day']),
                'dcls_end_day': parse_date(item.get('dcls_end_day')),
                'fin_co_subm_day': parse_datetime(item['fin_co_subm_day']),

            }
        )
        if created:
            saved_count += 1

    queryset = InvestmentProduct.objects.filter(type='적금').values()
    return Response({
        "message": f"{saved_count}개 저장됨",
        "products": list(queryset)
    })

@api_view(['POST'])
def save_etf_index_info(request):
    symbol = request.data.get('symbol')
    type_ = request.data.get('type')  # 'ETF' 또는 '지수'
    if not symbol or not type_:
        return Response({"error": "symbol, type 필수"}, status=400)
    data = fetch_etf_index_data(symbol, type_)
    obj, _ = DailyMarketData.objects.update_or_create(
        symbol=data['symbol'],
        record_date=data.get('record_date'),
        data_type=type_,
        defaults=data
    )
    return Response({"message": "저장 완료", "data": data})


@api_view(['GET'])
def get_etf_index_list(request):
    queryset = DailyMarketData.objects.all().values()
    return Response(list(queryset))


# 저장된 예·적금 상품 리스트를 JSON으로 반환
@api_view(['GET'])
def get_investment_product_list(request):
    products = InvestmentProduct.objects.all().values()
    return Response(list(products))

# 저장된 ETF/지수 시세 리스트를 JSON으로 반환
@api_view(['GET'])
def get_etf_market_list(request):
    data = DailyMarketData.objects.all().values()
    return Response(list(data))

@api_view(['GET'])
def kr_base_rate(request):
    ecos_key = 'HJBKWZETG3PZGYDHMMUH'
    today = date.today()
    end_month = today.strftime('%Y%m')
    start_year = today.year - 1
    start_month = f"{start_year}{today.month:02d}"
    url = (
        f"https://ecos.bok.or.kr/api/StatisticSearch/{ecos_key}/xml/kr/1/100/722Y001/M/{start_month}/{end_month}/0101000"
    )
    response = requests.get(url)
    response.encoding = 'utf-8'
    root = ET.fromstring(response.text)
    data = []
    for row in root.findall('./row'):
        date_str = row.findtext('TIME')
        value = row.findtext('DATA_VALUE')
        data.append((date_str, float(value)))
    # 최신값만 반환
    latest = data[-1] if data else (None, None)
    return Response({'date': latest[0], 'value': latest[1]})

@api_view(['GET'])
def us_base_rate(request):
    fred_key = '5111057dd0897bf1953e1ec8fa197afb'
    end_date = date.today()
    start_date = end_date - timedelta(days=365)
    url = (
        f"https://api.stlouisfed.org/fred/series/observations"
        f"?series_id=DFEDTARU"
        f"&api_key={fred_key}"
        f"&file_type=json"
        f"&observation_start={start_date}"
        f"&observation_end={end_date}"
    )
    response = requests.get(url)
    data = response.json()
    observations = data.get("observations", [])
    filtered = [obs for obs in observations if obs["value"] != "."]
    latest = filtered[-1] if filtered else {"date": None, "value": None}
    return Response({'date': latest["date"], 'value': float(latest["value"]) if latest["value"] else None})

@api_view(['GET'])
def usd_exchange_rate(request):
    ticker = yf.Ticker("USDKRW=X")
    data = ticker.history(period="1y")
    # 날짜별 환율 리스트 반환
    result = [
        {"date": str(idx.date()), "value": float(row["Close"])}
        for idx, row in data.iterrows()
    ]
    return Response(result)

