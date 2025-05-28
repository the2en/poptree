from django.apps import AppConfig
import os
import pandas as pd
from django.conf import settings
from .services import crawl_etf_detail
import json

class InvestmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'investments'
    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            return
        from .services import fetch_deposit_products, fetch_savings_products, fetch_etf_index_data, parse_date, parse_datetime
        from .models import InvestmentProduct, DailyMarketData, EtfDetail
        print("\n[서버 시작] 예금 상품 자동 조회 및 저장")
        base_list, rate_bounds, interest_detail = fetch_deposit_products()
        for item in base_list:
            code = item['fin_prdt_cd']
            lowest, highest = rate_bounds.get(code, (None, None))
            InvestmentProduct.objects.update_or_create(
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
        print("[서버 시작] 적금 상품 자동 조회 및 저장")
        base_list, rate_bounds, interest_detail = fetch_savings_products()
        for item in base_list:
            code = item['fin_prdt_cd']
            lowest, highest = rate_bounds.get(code, (None, None))
            InvestmentProduct.objects.update_or_create(
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
        
        # # ETF 상세정보 저장 (엑셀 기반)
        # BASE_DIR = settings.BASE_DIR
        # us_file = os.path.join(BASE_DIR, 'us_etf_list.xlsx')
        # kr_file = os.path.join(BASE_DIR, 'kr_etf_list.xlsx')

        '''print("[서버 시작] ETF 상세정보 저장 시작 (엑셀 기반)")
        for file, col in [(us_file, 'Symbol'), (kr_file, '단축코드')]:
            try:
                df = pd.read_excel(file)
                for code in df[col]:
                    try:
                        info = crawl_etf_detail(code)
                        if info:
                            etf_detail_data = {k: info.get(k) for k in [
                                'code', 'name', 'ticker', 'price_krw', 'price_usd', 'manager', 'marketcap',
                                'asset', 'issue', 'list_date', 'nav', 'fee', 'gap', 'summary']}

                            # holdings와 dividends를 JSON 문자열로 변환 시 ensure_ascii=False 적용
                            etf_detail_data['holdings'] = json.dumps(info.get('holdings', []), ensure_ascii=False)
                            etf_detail_data['dividends'] = json.dumps(info.get('dividends', []), ensure_ascii=False)

                            EtfDetail.objects.update_or_create(
                                code=etf_detail_data['code'],
                                defaults=etf_detail_data
                            )
                            print(f"[상세] {code} 저장 완료")
                        else:
                            print(f"[상세] {code} 정보 없음")
                    except Exception as e:
                        print(f"[상세] {code} 에러: {e}")
            except Exception as e:
                print(f"[상세] {file} 파일 에러: {e}")'''

        # print("[서버 시작] ETF 가격정보 저장 시작 (엑셀 기반)")
        # for file, col in [(us_file, 'Symbol'), (kr_file, '단축코드')]:
        #     try:
        #         df = pd.read_excel(file)
        #         for code in df[col]:
        #             try:
        #                 for row in fetch_etf_index_data(code, "ETF"):
        #                     daily_data = {k: row.get(k) for k in [
        #                         'symbol', 'name', 'data_type', 'record_date', 'close_price',
        #                         'daily_change_pct', 'high_52w', 'low_52w', 'aum'
        #                     ]}
        #                     DailyMarketData.objects.update_or_create(
        #                         symbol=daily_data['symbol'],
        #                         record_date=daily_data['record_date'],
        #                         data_type=daily_data['data_type'],
        #                         defaults=daily_data
        #                     )
        #                 print(f"[가격] {code} 저장 완료")
        #             except Exception as e:
        #                 print(f"[가격] {code} 에러: {e}")
        #     except Exception as e:
        #         print(f"[가격] {file} 파일 에러: {e}")
        # print("[서버 시작] ETF 상세정보 및 가격정보 자동 저장 완료")
        # # 필요하다면 DB 저장 등 추가 작업 가능