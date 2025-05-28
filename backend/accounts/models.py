from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # 기본 username 유지
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)

    # 기본 USERNAME_FIELD는 username이므로 설정 필요 없음
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.username
