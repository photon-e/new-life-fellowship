from django.views.generic import TemplateView

from .models import LiveStream


class LiveView(TemplateView):
    template_name = "live/live.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["live_stream"] = LiveStream.objects.filter(is_active=True).first() or LiveStream.objects.first()
        return context
