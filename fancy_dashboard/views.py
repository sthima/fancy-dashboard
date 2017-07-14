
from django.views.generic import TemplateView


class RootView(TemplateView):
    template_name = "dashboards/pull_requests.html"
