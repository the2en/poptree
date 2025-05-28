# ranking/utils/score_updater.py

from datetime import date
from django.utils.timezone import now
from spending.models import Spending
from accounts.models import User
from ranking.models import UserDailyRanking, RankingHistory
from spending.utils.classifier import get_spending_score

def update_user_daily_score(user, date):
    join_date = user.date_joined.date()  # 가입일 기준
    total_score = sum(
        get_spending_score(s.category or "")
        for s in Spending.objects.filter(user=user, date__date__gte=join_date)
    )

    UserDailyRanking.objects.update_or_create(
        user=user,
        record_date=date,
        defaults={"score": total_score}
    )


def update_global_ranking():
    today = now().date()
    scores = list(UserDailyRanking.objects.filter(record_date=today))

    # 현재 순위 기준 정렬
    scores.sort(key=lambda x: x.score, reverse=True)

    for rank, entry in enumerate(scores, start=1):
        user = entry.user

        # 기존 랭킹 불러오기
        previous = (
            RankingHistory.objects
            .filter(user=user)
            .order_by('-date')
            .first()
        )

        # 이전 순위와 비교하여 변화량 계산
        if previous:
            diff = previous.global_rank - rank
        else:
            diff = 0  # 첫 랭킹 기록이면 변화 없음

        # 현재 랭킹 저장
        RankingHistory.objects.update_or_create(
            user=user,
            date=today,
            defaults={
                "global_rank": rank,
                "rank_diff": diff
            }
        )