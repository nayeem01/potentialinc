from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer
from .permissions import IsCreatorOrReadOnly


class AllMoviesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)  # Link movie to the creator
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMoviesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        movies = Movie.objects.filter(created_by=request.user)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MovieDetailUpdateView(APIView):
    """
    API view to retrieve, update, or delete a movie instance.
    Only the creator of the movie can update or delete it.
    """

    permission_classes = [permissions.IsAuthenticated, IsCreatorOrReadOnly]

    def get_object(self, pk):
        movie = get_object_or_404(Movie, pk=pk)
        self.check_object_permissions(self.request, movie)
        return movie

    def get(self, request, pk, *args, **kwargs):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        movie = self.get_object(pk)
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        movie = self.get_object(pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieRatingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, movie_id, *args, **kwargs):
        """
        Create or update the user's rating for a specific movie.
        """
        movie = get_object_or_404(Movie, pk=movie_id)

        # Validate that `rating` is provided in the request data
        if "rating" not in request.data:
            return Response(
                {"error": "Rating value is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rating_value = request.data["rating"]
        if not (1 <= rating_value <= 5):
            return Response(
                {"error": "Rating must be between 1 and 5."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rating, created = Rating.objects.get_or_create(
            movie=movie,
            user=request.user,
            defaults={"rating": request.data["rating"]},
        )

        if not created:
            rating.rating = request.data["rating"]
            rating.save()

        serializer = RatingSerializer(rating, context={"request": request})

        movie.update_avg_rating()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
