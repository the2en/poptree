from django.db import models
from accounts.models import User

class Spending(models.Model):
    # 공통 필드
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()  # 실제 지출 금액
    date = models.DateTimeField()  # 승인일시 또는 거래일시
    category = models.CharField(max_length=80, blank=True)  # 추론된 소비 항목(예: 식비)
    source = models.CharField(max_length=10, choices=[('카드', '카드'), ('계좌', '계좌')])  # 출처 구분

    # 카드 전용 필드
    card_id = models.CharField(max_length=64, blank=True, null=True)
    merchant_name = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)  # 01: 승인, 02: 취소, 03: 정정

    # 계좌 전용 필드
    account_num = models.CharField(max_length=30, blank=True, null=True)
    trans_type = models.CharField(max_length=2, blank=True, null=True)  # 02: 출금, 03: 입금 등
    trans_memo = models.CharField(max_length=100, blank=True, null=True)

    # 해외결제나 외화 출금 등 통화 구분
    currency_code = models.CharField(max_length=5, default='KRW')

    def __str__(self):
        return f"{self.user.username} - {self.date.date()} - {self.amount}원 - {self.category or '미분류'}"

    
class MonthlySummary(models.Model):
    STATUS_CHOICES = [('정상', '정상'), ('초과', '초과')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)
    total_spending = models.IntegerField()
    
    def __str__(self):
        return f"{self.user.username} - {self.month}"