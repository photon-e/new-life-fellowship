from django.db import models
from django.urls import reverse


class Speaker(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    photo = models.ImageField(upload_to="speakers/", blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("speakers:detail", kwargs={"slug": self.slug})
