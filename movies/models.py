from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg

from decimal import Decimal, ROUND_HALF_UP


class Movie(models.Model):
    description = models.TextField()
    released_at = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    genre = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="movies"
    )
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_rating = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.description[:50]} - {self.language}"

    def update_avg_rating(self):
        """
        Update avg_rating based on all associated ratings, without modifying updated_at.
        """
        avg = self.ratings.aggregate(average=Avg("rating"))["average"] or 0
        total = self.ratings.count()
        avg_rating_decimal = Decimal(avg).quantize(
            Decimal("0.00"), rounding=ROUND_HALF_UP
        )

        Movie.objects.filter(pk=self.pk).update(
            avg_rating=avg_rating_decimal, total_rating=total
        )


class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("movie", "user")

    def __str__(self):
        return f"{self.user.username} rated {self.movie} - {self.rating}"


@receiver(post_save, sender=Rating)
def update_movie_avg_rating(sender, instance, **kwargs):
    instance.movie.update_avg_rating()
