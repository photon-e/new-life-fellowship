from django.db import models
from django.urls import reverse


class Video(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=280, unique=True)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to="videos/")
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True)
    speaker = models.ForeignKey(
        "speakers.Speaker",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="videos",
    )
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="videos",
    )
    topics = models.ManyToManyField("categories.Topic", blank=True, related_name="videos")
    duration = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("videos:detail", kwargs={"slug": self.slug})
