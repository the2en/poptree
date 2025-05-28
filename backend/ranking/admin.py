from django.contrib import admin
from .models import RankingHistory

@admin.register(RankingHistory)
class RankingHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'global_rank', 'rank_diff')
    list_filter = ('date',)
    search_fields = ('user__username',)
