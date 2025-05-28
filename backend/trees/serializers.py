from rest_framework import serializers
from .models import TreeStatus
from django.conf import settings

class TreeStatusSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = TreeStatus
        fields = ['current_level', 'good_spending_count', 'total_score', 'last_updated', 'image_url']

    def get_image_url(self, obj):
        return f"/static/trees/level_{obj.current_level}.png"
