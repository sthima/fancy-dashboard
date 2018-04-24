from django.views.generic import View
from braces.views import JSONResponseMixin

from fancy_dashboard.bitbucket.models import BitbucketClient, GithubClient
from fancy_dashboard.dashboard.models.pullrequests import PullRequest as PullRequestModel
from ..utils import get_bitbucket_pullrequests, get_github_pullrequests


class LoadPullRequestJsonView(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        for client in BitbucketClient.objects.all():
            get_bitbucket_pullrequests(
                client,
            )
        for client in GithubClient.objects.all():
            get_github_pullrequests(
                client,
            )

        return self.render_json_response([])


# TODO serializer
class PullRequestDashboardJsonView(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        pull_requests = []
        for pullrequest in PullRequestModel.objects.all():
            pull_requests += [{
                'updated_on': pullrequest.updated_on,
                'updated_by': pullrequest.updated_by,
                'key': pullrequest.key,
                'author': pullrequest.author,
                'task_count': pullrequest.task_count,
                'build_count': pullrequest.build_count,
                'last_build': pullrequest.last_build,
                'url': pullrequest.url,
                'approvals': [{
                    'display_name': approval.display_name,
                    'avatar': approval.avatar,
                } for approval in pullrequest.approvals.all()],
            }]

        return self.render_json_response(pull_requests)
