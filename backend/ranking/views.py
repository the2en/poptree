from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import User
from spending.models import Spending
from spending.utils.classifier import get_spending_score
from django.utils.timezone import now
from .models import RankingHistory, UserDailyRanking
from django.db.models import F

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_score(request):
    user = request.user
    score = sum(get_spending_score(s.category or "") for s in Spending.objects.filter(user=user))
    return Response({"username": user.username, "score": score})


@api_view(['GET'])
def leaderboard(request):
    scores = []
    for user in User.objects.all():
        total = sum(get_spending_score(s.category or "") for s in Spending.objects.filter(user=user))
        scores.append({"username": user.username, "score": total})

    scores.sort(key=lambda x: x["score"], reverse=True)
    return Response(scores)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_ranking(request):
    user = request.user
    today = now().date()
    # 상위 10명 랭킹
    today_rankings = (
        RankingHistory.objects.filter(date=today)
        .order_by('global_rank')[:10]
    )
    ranking_list = [
        {
            'username': rh.user.username,
            'rank': rh.global_rank,
            'score': float(UserDailyRanking.objects.filter(user=rh.user, record_date=today).first().score) if UserDailyRanking.objects.filter(user=rh.user, record_date=today).exists() else None,
            'rank_diff': rh.rank_diff
        }
        for rh in today_rankings
    ]
    # 내 랭킹
    my_rh = RankingHistory.objects.filter(user=user, date=today).first()
    my_score = UserDailyRanking.objects.filter(user=user, record_date=today).first()
    my_ranking = None
    if my_rh and my_score:
        my_ranking = {
            'username': user.username,
            'rank': my_rh.global_rank,
            'score': float(my_score.score),
            'rank_diff': my_rh.rank_diff
        }
    total_users = RankingHistory.objects.filter(date=today).count()
    return Response({
        'date': str(today),
        'total_users': total_users,
        'my_ranking': my_ranking,
        'ranking_list': ranking_list
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ranking_history(request):
    user = request.user
    qs = RankingHistory.objects.filter(user=user).order_by('date')
    history = [
        {'date': str(rh.date), 'rank': rh.global_rank, 'score': float(UserDailyRanking.objects.filter(user=user, record_date=rh.date).first().score) if UserDailyRanking.objects.filter(user=user, record_date=rh.date).exists() else None}
        for rh in qs
    ]
    return Response({
        'username': user.username,
        'history': history
    })
