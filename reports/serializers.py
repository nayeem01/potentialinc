from rest_framework import serializers
from .models import MovieReport


class MovieReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReport
        fields = ["id", "movie", "reported_by", "reason", "status", "reported_at"]
        read_only_fields = ["movie", "reported_by", "status", "reported_at"]
