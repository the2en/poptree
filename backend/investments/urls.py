from django.urls import path
from .views import (
    get_investment_product_list,
    get_etf_market_list,
    kr_base_rate,
    us_base_rate,
    usd_exchange_rate
)
from gpt import gpt_answer

urlpatterns = [
    path('products/list/', get_investment_product_list, name='investment_product_list'),
    path('market/list/', get_etf_market_list, name='etf_market_list'),
    path('kr-base-rate/', kr_base_rate),
    path('us-base-rate/', us_base_rate),
    path('exchange-rate/usd/', usd_exchange_rate),
    path('gpt/answer/', gpt_answer),
]
