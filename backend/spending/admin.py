from django.contrib import admin
from .models import Spending, MonthlySummary

@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date')
    list_filter = ('category', 'date')
    search_fields = ('user__username',)

@admin.register(MonthlySummary)
class MonthlySummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'total_spending')
    list_filter = ('month',)
    search_fields = ('user__username',)
