import logging
import os

import arrow
import requests
from pybitbucket.bitbucket import Client
from pybitbucket.pullrequest import PullRequest
from pybitbucket.repository import Repository
from pybitbucket.auth import BasicAuthenticator

from fancy_dashboard.dashboard.models.pullrequests import PullRequest as PullRequestModel, PullRequestApproval

log = logging.getLogger(__name__)

BITBUCKET_ENDPOINT = 'https://api.bitbucket.org/2.0/repositories{/owner}{?q}'
GITHUB_ENDPOINT = "https://api.github.com/graphql"

GITHUB_PR_QUERY = open(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "..",
    "queries",
    "github",
    "pullrequests.gql")).read()


def get_user_for_activity(activity):
    for value in activity.values():
        if 'user' in value:
            return value['user']
        elif 'author' in value:
            return value['author']


# def get_pullrequests(username, password, email):
def get_bitbucket_pullrequests(client):
    bitbucket = Client(
        BasicAuthenticator(
            client.username,  # Username
            client.password,  # Password/API Key
            client.email,  # E-mail
        )
    )

    repositories = bitbucket.remote_relationship(
        BITBUCKET_ENDPOINT,
        owner=client.username,
        q='project.key="ACTIVE"',
    )

    existing_keys = []

    for repo in repositories:
        repo = repo.slug
        log.error("Repository: %s" % repo)
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
            pull_request.url = pr.links['html']['href']
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


def get_github_pullrequests(client):
    headers = {"Authorization": "Bearer {}".format(client.token)}

    variables = {
        "login": client.username
    }

    response = requests.post(
        GITHUB_ENDPOINT,
        json={ "query": GITHUB_PR_QUERY, "variables": variables},
        headers=headers)

    if response.status_code != 200:
        log.error("HTTP error while trying to fetch GitHub PRs")
        return

    json_data, errors = response.json()["data"], response.json().get("errors")
    if errors:
        log.error("GraphQL error while trying to fetch GitHub PRs:\n")
        log.error(errors)
        return

    existing_keys = []
    for repository in json_data["organization"]["repositories"]["nodes"]:
        for pull_request in repository["pullRequests"]["nodes"]:
            if pull_request["state"] != "OPEN":
                continue

            key = "{}-{}".format(repository['name'], pull_request['number'])
            existing_keys.append(key)
            db_pull_request = PullRequestModel.objects.filter(client=client) \
                                              .filter(key=key).first()

            if not db_pull_request:
                db_pull_request = PullRequestModel()
                db_pull_request.key = key
                db_pull_request.client = client

            db_pull_request.updated_on = pull_request["updatedAt"]
            db_pull_request.author = pull_request["author"]["login"]
            db_pull_request.url = pull_request["url"]

            # NOTE (mmarchini: We don't have this info yet, so keep those fields
            # empty.
            db_pull_request.updated_by = "unknown"
            db_pull_request.task_count = 0
            db_pull_request.build_count = 0
            db_pull_request.last_build = None

            db_pull_request.save()

            if db_pull_request.approvals.count():
                db_pull_request.approvals.all().delete()

            for a in pull_request["reviews"]["nodes"]:
                author = a['author']
                approval = PullRequestApproval()
                approval.display_name = author["login"]
                approval.avatar = author["avatarUrl"]
                approval.pullrequest = db_pull_request
                approval.save()

    PullRequestModel.objects.filter(client=client).exclude(key__in=existing_keys).all().delete()
