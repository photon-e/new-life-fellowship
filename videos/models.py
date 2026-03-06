from django.db import models
from django.urls import reverse

from categories.models import Category


class Video(models.Model):
    class Visibility(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True)
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.DRAFT)
    is_featured = models.BooleanField(default=False)

    primary_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_videos',
    )
    categories = models.ManyToManyField(Category, related_name='videos', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['visibility', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('videos:detail', kwargs={'slug': self.slug})
