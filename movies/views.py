from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer

from .permissions import IsCreatorOrReadOnly


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def perform_create(self, serializer):
        """Associate the created movie with the current user."""
        serializer.save(created_by=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Rating.objects.filter(movie_id=self.kwargs["movie_pk"])

    def perform_create(self, serializer):
        """Ensure the user can rate the movie and update avg_rating on the Movie model."""
        movie = get_object_or_404(Movie, id=self.kwargs["movie_pk"])
        rating, created = Rating.objects.update_or_create(
            movie=movie,
            user=self.request.user,
            defaults={"rating": serializer.validated_data["rating"]},
        )
        # Trigger avg_rating recalculation
        movie.calculate_avg_rating()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
