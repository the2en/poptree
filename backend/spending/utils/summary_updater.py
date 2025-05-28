# spending/utils/summary_updater.py

from django.db.models import Sum
from spending.models import Spending, MonthlySummary

def update_monthly_summary(user):
    data = (
        Spending.objects.filter(user=user)
        .values_list("date__year", "date__month")
        .annotate(total=Sum("amount"))
    )

    for year, month, total in data:
        month_str = f"{year}-{month:02d}"
        MonthlySummary.objects.update_or_create(
            user=user,
            month=month_str,
            defaults={"total_spending": total}
        )
