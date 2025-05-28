from django.contrib import admin
from .models import InvestmentProduct

@admin.register(InvestmentProduct)
class InvestmentProductAdmin(admin.ModelAdmin):
    list_display = (
        'kor_co_nm',         # 금융사명
        'fin_prdt_nm',       # 상품명 (이전의 name)
        'type',              # 예금/적금
        'lowest_rate',
        'highest_rate',
        'fin_prdt_cd',       # 상품 코드 (이전의 external_product_id)
    )
    search_fields = ('fin_prdt_nm', 'kor_co_nm')
    list_filter = ('type',)
