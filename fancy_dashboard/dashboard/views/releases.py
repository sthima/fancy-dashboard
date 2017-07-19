from django.views.generic import View
from braces.views import JSONResponseMixin

from fancy_dashboard.dashboard.models.releases import Release


# TODO serializer
class ReleaseDashboardJsonView(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        releases = []
        for release in Release.objects.all():
            releases += [{
                'project': release.project,
                'version': release.version,
                'statuses': [{
                    'status': release_status.status,
                    'count': release_status.count,
                    'style': release_status.style,
                } for release_status in release.statuses.all()],
            }]

        return self.render_json_response(releases)
