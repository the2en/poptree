# accounts/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
import logging
logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        logger.warning("✅ save_user 호출됨")

        user = super().save_user(request, user, form, commit=False)

        # form.cleaned_data에서 name 추출, 없으면 request에서 가져오기
        name_value = form.cleaned_data.get('name') or request.data.get('name')
        logger.warning(f"✅ name 값: {name_value}")

        user.name = name_value or ''  # ← 이 줄이 반드시 있어야 null 에러 방지됨

        if commit:
            user.save()
        return user
