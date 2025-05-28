from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # 관리자 리스트에서 보일 필드들
    list_display = ('username', 'email', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    # 유저 생성/수정 페이지에서 보여줄 필드 그룹
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('개인 정보', {'fields': ('email', 'name')}),
        ('권한', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('중요 날짜', {'fields': ('last_login', 'date_joined')}),
    )

    # 새 유저 생성 페이지에서 보여줄 필드들
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('username', 'email', 'name')
    ordering = ('username',)
