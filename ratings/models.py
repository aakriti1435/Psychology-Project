from django.db import models


class RatingReviews(models.Model):
    rating = models.FloatField(null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    image = models.ImageField(upload_to='rating_user/', blank=True, null=True)

    class Meta:
        managed = True
        db_table = "tbl_ratings"


