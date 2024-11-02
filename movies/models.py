from django.db import models
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, F, Sum


class Movie(models.Model):
    description = models.TextField()
    released_at = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    genre = models.CharField(max_length=50)
    # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="movies")
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_rating = models.PositiveIntegerField(default=0)
    language = models.CharField(max_length=30)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.description)[:50]} - {self.language}"

    def calculate_avg_rating(self):
        """Calculate and update the avg_rating based on current ratings."""
        avg = self.ratings.aggregate(average=Avg("rating"))["average"] or 0
        total = self.ratings.count()
        self.avg_rating = round(avg, 2)
        self.total_rating = total
        self.save(update_fields=["avg_rating", "total_rating"])


class Rating(models.Model):
    movie = models.ForeignKey(Movie, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )  # Ratings from 1 to 5
    rated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "movie",
            "user",
        )

    def __str__(self):
        return f"{self.user.username} rated {self.movie} - {self.rating}"

    def save(self, *args, **kwargs):
        """Override save to recalculate avg_rating after each rating is created/updated."""
        super().save(*args, **kwargs)
        self.movie.calculate_avg_rating()
