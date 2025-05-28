from django.contrib import admin
from .models import TreeStatus

@admin.register(TreeStatus)
class TreeStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_level', 'last_updated')
    list_filter = ('current_level',)
    search_fields = ('user__username',)
