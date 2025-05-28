from django.db import models
from accounts.models import User

class RankingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    global_rank = models.IntegerField()
    rank_diff = models.IntegerField(help_text="양수: 상승, 음수: 하락")

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.global_rank}위 ({self.rank_diff:+})"

class UserDailyRanking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record_date = models.DateField()
    score = models.DecimalField(max_digits=20, decimal_places=4)

    class Meta:
        unique_together = (('user', 'record_date'),)

    def __str__(self):
        return f"{self.user.username} - {self.record_date} - {self.score}"
