from django.urls import path
from . import views
from .views import today_ranking, ranking_history

urlpatterns = [
    path('score/', views.user_score, name='user-score'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('today/', today_ranking),
    path('history/', ranking_history),
]
