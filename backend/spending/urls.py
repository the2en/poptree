from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.spending_daily, name='spending-daily'),
    path('by-category/', views.by_category_view, name='spending-by-category'),
    path('calendar/', views.calendar_view, name='spending-calendar'),
    path('statistics/', views.spending_statistics, name='spending-statistics'),
]
