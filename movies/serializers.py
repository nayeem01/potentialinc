from rest_framework import serializers
from .models import Movie, Rating

from pytz import timezone as pytz_timezone


class MovieSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    avg_rating = serializers.ReadOnlyField()
    total_rating = serializers.ReadOnlyField()

    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "description",
            "released_at",
            "duration",
            "genre",
            "created_by",
            "avg_rating",
            "total_rating",
            "language",
        ]

    # Convert `created_at` to Bangladesh timezone
    def get_created_at(self, obj):
        bd_timezone = pytz_timezone("Asia/Dhaka")
        return obj.created_at.astimezone(bd_timezone).strftime("%Y-%m-%d %H:%M:%S")

    def get_updated_at(self, obj):
        bd_timezone = pytz_timezone("Asia/Dhaka")
        return obj.updated_at.astimezone(bd_timezone).strftime("%Y-%m-%d %H:%M:%S")


class RatingSerializer(serializers.ModelSerializer):
    rated_at = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ["id", "movie", "user", "rating", "rated_at"]
        read_only_fields = ["user", "rated_at"]

    # Convert `rated_at` to Bangladesh timezone
    def get_rated_at(self, obj):
        bd_timezone = pytz_timezone("Asia/Dhaka")
        return obj.rated_at.astimezone(bd_timezone).strftime("%Y-%m-%d %H:%M:%S")

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)
