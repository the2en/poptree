# ranking/management/commands/update_ranking.py

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from accounts.models import User
from ranking.models import UserDailyRanking, RankingHistory
from ranking.utils.score_updater import update_user_daily_score

class Command(BaseCommand):
    help = "모든 유저의 일일 점수와 랭킹을 저장합니다."

    def handle(self, *args, **options):
        today = now().date()

        # 1. 모든 유저 점수 저장
        for user in User.objects.all():
            score = update_user_daily_score(user, today)
            self.stdout.write(f"✅ {user.username} 점수 저장: {score}")

        # 2. 랭킹 계산 및 RankingHistory 저장
        rankings = (
            UserDailyRanking.objects
            .filter(record_date=today)
            .order_by('-score')
        )

        for rank, record in enumerate(rankings, start=1):
            prev = RankingHistory.objects.filter(user=record.user).order_by('-date').first()
            prev_rank = prev.global_rank if prev else None
            diff = 0 if prev_rank is None else prev_rank - rank

            RankingHistory.objects.create(
                user=record.user,
                date=today,
                global_rank=rank,
                rank_diff=diff
            )
            self.stdout.write(f"🏆 {record.user.username} → {rank}위 ({diff:+})")
