import arrow
from pybitbucket.bitbucket import Client
from pybitbucket.pullrequest import PullRequest
from pybitbucket.repository import Repository
from pybitbucket.auth import BasicAuthenticator

from fancy_dashboard.dashboard.models.pullrequests import PullRequest as PullRequestModel, PullRequestApproval


def get_user_for_activity(activity):
    for value in activity.values():
        if 'user' in value:
            return value['user']
        elif 'author' in value:
            return value['author']


# def get_pullrequests(username, password, email):
def get_pullrequests(client):
    bitbucket = Client(
        BasicAuthenticator(
            client.username,  # Username
            client.password,  # Password/API Key
            client.email,  # E-mail
        )
    )

    repositories = [repo.slug for repo in Repository.find_repositories_by_owner_and_role(role='owner', client=bitbucket)]
    existing_keys = []

    for repo in repositories:
        for pr in PullRequest.find_pullrequests_for_repository_by_state(repo, client=bitbucket):
            if type(pr) == dict:
                continue
            pull_request_key = "{repo}-{pr_id}".format(repo=repo.upper(), pr_id=pr.id)
            existing_keys.append(pull_request_key)
            pull_request = PullRequestModel.objects.filter(client=client).filter(key=pull_request_key).first()

            if not pull_request:
                pull_request = PullRequestModel()
                pull_request.key = pull_request_key
                pull_request.client = client

            activity = list(pr.activity())

            # Get last update
            pull_request.updated_on = arrow.get(pr.updated_on).datetime
            pull_request.updated_by = get_user_for_activity(activity[0])['display_name']

            # Get author
            pull_request.author = pr.author.display_name

            # Get task count
            pull_request.task_count = pr.task_count

            # Get last build
            statuses = list(pr.statuses())
            if 'pagelen' in statuses[0]:
                statuses.pop()
            statuses = sorted(statuses, key=lambda s: arrow.get(s['updated_on']).datetime, reverse=True)
            print("Build count:", len(statuses))
            pull_request.build_count = len(statuses)
            pull_request.last_build = None
            if len(statuses):
                pull_request.last_build = statuses[0]['state']
            pull_request.save()

            if pull_request.approvals.count():
                pull_request.approvals.all().delete()

            # Get approvals
            approvals = filter(lambda a: 'approval' in a, activity)
            for a in approvals:
                approval = PullRequestApproval()
                approval.display_name = a['approval']['user']['display_name']
                approval.avatar = a['approval']['user']['links']['avatar']['href']
                approval.pullrequest = pull_request
                approval.save()
    PullRequestModel.objects.filter(client=client).exclude(key__in=existing_keys).all().delete()
