from rest_framework import serializers
from .models import MovieReport

from pytz import timezone as pytz_timezone


class MovieReportSerializer(serializers.ModelSerializer):
    reported_at = serializers.SerializerMethodField()

    class Meta:
        model = MovieReport
        fields = ["id", "movie", "reported_by", "reason", "status", "reported_at"]
        read_only_fields = ["movie", "reported_by", "status", "reported_at"]

    def get_reported_at(self, obj):
        bd_timezone = pytz_timezone("Asia/Dhaka")
        reported_at_in_bd = obj.reported_at.astimezone(bd_timezone)
        return reported_at_in_bd.strftime("%Y-%m-%d %H:%M:%S")
