from rest_framework import serializers
from .models import Movie, Rating


class MovieSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source="created_by.username")
    avg_rating = serializers.ReadOnlyField()
    total_rating = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "description",
            "released_at",
            "duration",
            "genre",
            "created_by",
            "avg_rating",
            "total_rating",
            "language",
            "created_at",
            "updated_at",
        ]


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ["id", "movie", "user", "rating", "rated_at"]
