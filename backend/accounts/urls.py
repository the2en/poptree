from django.urls import path, include
from . import views

urlpatterns = [
    # 사용자 정보 조회/수정/삭제
    path('userinfo/<str:username>/', views.user_detail),
    path('update/<str:username>/', views.update_user),
    path('delete/', views.delete_user),

    # 로그인/회원가입/로그아웃
    path('auth/login/', views.login_view, name='custom_login'),  # 만든 함수형 로그인 뷰
    path('auth/', include('dj_rest_auth.urls')),  # 나머지 logout, password change 등
    path('auth/signup/', include('dj_rest_auth.registration.urls')),  # 회원가입
]
