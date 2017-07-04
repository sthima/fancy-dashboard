import arrow
from pybitbucket.bitbucket import Client
from pybitbucket.pullrequest import PullRequest
from pybitbucket.auth import BasicAuthenticator

bitbucket = Client(
    BasicAuthenticator(
        '',  # Username
        '',  # Password/API Key
        '',  # E-mail
    )
)


def get_user_for_activity(activity):
    for value in activity.values():
        if 'user' in value:
            return value['user']
        elif 'author' in value:
            return value['author']


for repo in ['netell', 'encanto']:
    print("------- {repo} -------".format(repo=repo))
    for pr in PullRequest.find_pullrequests_for_repository_by_state(repo, client=bitbucket):
        print("...")

        activity = list(pr.activity())

        # Get approvals
        approvals = filter(lambda a: 'approval' in a, activity)
        print("Approvers:", [(a['approval']['user']['display_name'], a['approval']['user']['links']['avatar']) for a in approvals])

        # Get last update
        print("Updated on:", arrow.get(pr.updated_on).datetime)
        print("Updated by:", get_user_for_activity(activity[0])['display_name'])

        # Get author
        print("Author:", pr.author['display_name'])

        #
        print("Key:", "{repo}-{pr_id}".format(repo=repo.upper(), pr_id=pr.id))

        # Get task count
        print("Task count:", pr.task_count)

        # Get last build
        statuses = list(pr.statuses())
        if 'pagelen' in statuses[0]:
            statuses.pop()
        statuses = sorted(statuses, key=lambda s: arrow.get(s['updated_on']).datetime, reverse=True)
        print("Build count:", len(statuses))
        if len(statuses):
            print("Last build status:", statuses[0]['state'])

print("allgood")
