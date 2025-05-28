from django.db import models
from django.conf import settings
from datetime import date

class InvestmentProduct(models.Model):
    # 기본 정보
    fin_prdt_cd = models.CharField(max_length=50, unique=True)  # 상품 코드
    fin_co_no = models.CharField(max_length=20)                 # 금융사 코드
    kor_co_nm = models.CharField(max_length=100)                # 금융사 이름
    fin_prdt_nm = models.CharField(max_length=100)              # 상품 이름
    type = models.CharField(max_length=10)                      # '예금' or '적금'

    # 가입 조건 및 설명
    join_way = models.TextField()                               # 가입 방법 (영업점/인터넷/스마트폰 등)
    join_deny = models.CharField(max_length=10)                 # 가입 제한 여부 (1: 가능)
    join_member = models.TextField()                            # 가입 대상
    spcl_cnd = models.TextField(null=True, blank=True)          # 우대 조건
    etc_note = models.TextField(null=True, blank=True)          # 기타 설명
    mtrt_int = models.TextField(null=True, blank=True)          # 만기 후 이자 설명

    # 금리 및 조건
    intr_rate_type_nm = models.CharField(max_length=20, null=True, blank=True)  # 단리/복리
    max_limit = models.BigIntegerField(null=True, blank=True)   # 최대 가입 금액
    interest_detail = models.JSONField(default=dict)            # 기간별 금리 정보 (optionList 기반)

    # 금리 요약 정보
    lowest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    highest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    # 공시 정보
    dcls_month = models.CharField(max_length=10)                # 공시월 (예: 202504)
    dcls_strt_day = models.DateField()                          # 공시 시작일
    dcls_end_day = models.DateField(null=True, blank=True)      # 공시 종료일
    fin_co_subm_day = models.DateTimeField()                    # 금융사 제출일
    record_date = models.DateField(default=date.today)           # 상품 정보가 DB에 입력/업데이트된 날짜

    def __str__(self):
        return f"{self.kor_co_nm} - {self.fin_prdt_nm}"

class DailyMarketData(models.Model):
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    data_type = models.CharField(max_length=20)  # 'ETF', 'INDEX', 'CURRENCY', 'INTEREST_RATE' 등
    record_date = models.DateField()  # 해당 데이터가 기록된 날짜
    close_price = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)  # 종가
    daily_change_pct = models.DecimalField(max_digits=7, decimal_places=4, null=True, blank=True)  # 등락률(%)
    high_52w = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    low_52w = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    aum = models.BigIntegerField(null=True, blank=True)  # ETF만 해당

    class Meta:
        unique_together = (('symbol', 'record_date', 'data_type'),)

    def __str__(self):
        return f"{self.symbol} ({self.data_type}) - {self.record_date}"

class EtfDetail(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    ticker = models.CharField(max_length=20, null=True, blank=True)
    price_krw = models.CharField(max_length=30, null=True, blank=True)
    price_usd = models.CharField(max_length=30, null=True, blank=True)
    manager = models.CharField(max_length=50, null=True, blank=True)
    marketcap = models.CharField(max_length=50, null=True, blank=True)
    asset = models.CharField(max_length=50, null=True, blank=True)
    issue = models.CharField(max_length=50, null=True, blank=True)
    list_date = models.CharField(max_length=30, null=True, blank=True)
    nav = models.CharField(max_length=30, null=True, blank=True)
    fee = models.CharField(max_length=30, null=True, blank=True)
    gap = models.CharField(max_length=30, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    holdings = models.JSONField(default=list, blank=True)  # Top 10 보유종목
    dividends = models.JSONField(default=list, blank=True) # 배당내역
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
