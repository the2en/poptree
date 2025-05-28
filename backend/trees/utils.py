from spending.models import Spending
from ranking.models import UserDailyRanking
from .models import TreeStatus
from spending.utils.classifier import GOOD_CATEGORIES
from django.db.models import Sum

def update_tree_status(user):
    # 전체 누적 점수 (단, 점수는 음수 가능 → 하락 가능)
    score_sum = UserDailyRanking.objects.filter(user=user).aggregate(Sum('score'))['score__sum'] or 0

    # 전체 좋은 소비 횟수
    good_count = Spending.objects.filter(
        user=user,
        category__in=GOOD_CATEGORIES
    ).count()

    # 트리 단계 계산
    if score_sum >= 750:
        level = 10
    elif score_sum >= 580:
        level = 9
    elif score_sum >= 450:
        level = 8
    elif score_sum >= 350:
        level = 7
    elif score_sum >= 250:
        level = 6
    elif score_sum >= 180:
        level = 5
    elif score_sum >= 120:
        level = 4
    elif score_sum >= 70:
        level = 3
    elif score_sum >= 30:
        level = 2
    else:
        level = 1

    tree_status, _ = TreeStatus.objects.get_or_create(user=user)
    tree_status.good_spending_count = good_count
    tree_status.total_score = score_sum
    tree_status.current_level = level
    tree_status.save()
