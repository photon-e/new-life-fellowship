from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.videos.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("live/", include("apps.live.urls")),
    path("videos/", include("apps.videos.urls")),
    path("speakers/", include("apps.speakers.urls")),
    path("topics/", include("apps.categories.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
