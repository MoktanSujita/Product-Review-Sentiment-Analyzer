from django.db import models


# Create your models here.
class Review(models.Model):
    product_name = models.CharField(max_length=200)
    product_url = models.URLField()
    sentiment = models.CharField(max_length=50, blank=True)  # e.g., Positive / Negative / Neutral
    analyzed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.sentiment}"
