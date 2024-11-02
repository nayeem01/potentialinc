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
    class Meta:
        model = Rating
        fields = ["id", "movie", "user", "rating", "rated_at"]
        read_only_fields = ["user", "rated_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)
