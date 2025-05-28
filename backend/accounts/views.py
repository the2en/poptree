# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer

from spending.utils.dummy_generator import generate_dummy_spending
from spending.utils.summary_updater import update_monthly_summary

# 사용자 정보 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# 사용자 정보 수정
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserSerializer(instance=user, data=request.data, partial=True) # partial=True: 일부 필드만 수정
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)

# 사용자 삭제 (자기 자신 계정 삭제)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'message': '계정이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # 로그인 성공 후 더미 업데이트
        generate_dummy_spending(user, initial=False)

        # 로그인 성공 후 월별 소비 요약 갱신
        update_monthly_summary(user)

        # JWT 토큰 발급
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        user_data = UserSerializer(user).data

        return Response({
            "message": "로그인 성공",
            "user": user_data,
            "access": access_token,
            "refresh": refresh_token
        }, status=200)
    else:
        return Response({
            "error": "아이디 또는 비밀번호가 올바르지 않습니다."
        }, status=status.HTTP_401_UNAUTHORIZED)