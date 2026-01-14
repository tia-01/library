from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.

class Book(models.Model):
    genre_choices = [
        ('fiction', "fiction"),
        ('non-fiction', "non-fiction"),
        ('mystery', "mystery"),
        ('science', "science"),
        ('biography', "biography"),
    ]
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=20)
    isbn = models.IntegerField(unique=True, blank=True, null=True)
    published_date = models.DateField(null=True, blank=True)
    genre = models.CharField(choices=genre_choices)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.published_date and self.published_date > timezone.now().date():
            raise ValidationError("Published date cannot be in the future.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    