from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from spending.models import Spending
from django.db.models import Sum
from django.utils.timezone import localdate
from datetime import timedelta, datetime


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spending_daily(request):
    """
    일자별 소비 금액 합계 (Line Chart)
    """
    user = request.user
    queryset = (
        Spending.objects
        .filter(user=user)
        .values('date__date')
        .annotate(total=Sum('amount'))
        .order_by('date__date')
    )
    return Response(queryset)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def by_category_view(request):
    """
    카테고리별 소비 금액 (Pie Chart)
    """
    user = request.user
    queryset = (
        Spending.objects
        .filter(user=user)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    return Response(queryset)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calendar_view(request):
    """
    달력용: 날짜별 소비 금액
    """
    user = request.user
    queryset = (
        Spending.objects
        .filter(user=user)
        .values('date__date')
        .annotate(total=Sum('amount'))
        .order_by('date__date')
    )
    return Response([
        {"date": item["date__date"], "amount": item["total"]} for item in queryset
    ])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def spending_statistics(request):
    """
    더미데이터(Spending) 기준 연/월/일별 소비 통계, 카테고리별 합계, 일별 상세 항목 반환
    쿼리파라미터: year, month (예: ?year=2023&month=10)
    """
    user = request.user
    year = int(request.GET.get('year', datetime.now().year))
    month = int(request.GET.get('month', datetime.now().month))

    # 해당 연월의 모든 소비 데이터
    spendings = Spending.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    )

    # 일별 데이터
    daily_data = []
    for day in range(1, 32):
        day_spendings = spendings.filter(date__day=day)
        if not day_spendings.exists():
            continue
        total_spending = day_spendings.aggregate(total=Sum('amount'))['total'] or 0
        # 카테고리별 분포
        categories = (
            day_spendings.values('category')
            .annotate(amount=Sum('amount'))
            .order_by('-amount')
        )
        daily_data.append({
            "date": f"{year}-{month:02d}-{day:02d}",
            "total_spending": total_spending,
            "categories": [
                {"category": c["category"], "amount": c["amount"]} for c in categories
            ],
            "details": [
                {
                    "amount": s.amount,
                    "category": s.category,
                    "source": s.source,
                    "merchant_name": s.merchant_name,
                    "account_num": s.account_num,
                    "currency_code": s.currency_code,
                }
                for s in day_spendings
            ]
        })

    # 월 전체 카테고리별 합계
    category_summary_qs = (
        spendings.values('category')
        .annotate(amount=Sum('amount'))
        .order_by('-amount')
    )
    total_spending = spendings.aggregate(total=Sum('amount'))['total'] or 0
    category_summary = [
        {
            "category": item['category'],
            "amount": item['amount']
        }
        for item in category_summary_qs
    ]

    return Response({
        "year": year,
        "month": month,
        "total_spending": total_spending,
        "daily": daily_data,
        "category_summary": category_summary
    })
