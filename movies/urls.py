from django.urls import path
from .views import MovieDetailUpdateView, AllMoviesView, UserMoviesView, MovieRatingView

urlpatterns = [
    path("allmovies/", AllMoviesView.as_view(), name="all-movies"),
    path("movies/user/", UserMoviesView.as_view(), name="user-movies"),
    path(
        "movie/<int:pk>/",
        MovieDetailUpdateView.as_view(),
        name="update-movie-detail",
    ),
    path("movie/<int:movie_id>/rate/", MovieRatingView.as_view(), name="movie-rate"),
]
