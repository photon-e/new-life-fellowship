from django.db import models


class LiveStream(models.Model):
    title = models.CharField(max_length=255)
    stream_url = models.URLField(help_text="Direct stream URL or hosted MP4/HLS URL")
    current_program = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_active", "-updated_at"]

    def __str__(self):
        return self.title
