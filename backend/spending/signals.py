from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from accounts.models import User
from spending.models import Spending
from spending.utils.dummy_generator import generate_dummy_spending
from ranking.utils.score_updater import update_user_daily_score, update_global_ranking
from trees.utils import update_tree_status


# 회원가입 시 더미 소비 데이터만 생성 (점수는 0으로 시작)
@receiver(post_save, sender=User)
def create_spending_on_signup(sender, instance, created, **kwargs):
    if created:
        generate_dummy_spending(instance, initial=True)
        # 점수 저장은 하지 않음 → 가입 이후부터 집계

# 소비 생성 또는 삭제 시 → 점수 및 전체 랭킹 갱신
@receiver([post_save, post_delete], sender=Spending)
def update_ranking_on_spending_change(sender, instance, **kwargs):
    today = now().date()
    update_user_daily_score(instance.user, today)
    update_global_ranking()

# 소비 발생 시 TreeStatus 자동 갱신
@receiver([post_save, post_delete], sender=Spending)
def update_tree_on_spending_change(sender, instance, **kwargs):
    update_tree_status(instance.user)