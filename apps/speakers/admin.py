from django.contrib import admin

from .models import Speaker


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "bio")
    prepopulated_fields = {"slug": ("name",)}
