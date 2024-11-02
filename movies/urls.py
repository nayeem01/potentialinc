# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, RatingViewSet

router = DefaultRouter()
router.register(r"movies", MovieViewSet)

movie_rating = RatingViewSet.as_view({"post": "create", "get": "list"})

urlpatterns = [
    path("", include(router.urls)),
    path("movies/<int:movie_pk>/ratings/", movie_rating, name="movie-ratings"),
]
