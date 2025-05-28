from django.db import models
from accounts.models import User

class TreeStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_level = models.IntegerField(default=1)
    good_spending_count = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Level {self.current_level}"