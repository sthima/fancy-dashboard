from jira import JIRA
from collections import OrderedDict

from ..models.releases import Release, ReleaseStatus


# TODO user should configure that
STATUSES = OrderedDict([
    ('Open', {
        'statuses': ['Open', 'Backlog', 'Selected for Development', ],
        'style': 'purple',
    }),
    ('WIP', {
        'statuses': ['In Progress', 'Waiting Pull Request', ],
        'style': 'light-blue',
    }),
    ('PR', {
        'statuses': ['Code Revision', ],
        'style': 'yellow',
    }),
    ('Test', {
        'statuses': ['To Test', 'Testing', ],
        'style': 'green',
    }),
    ('Done', {
        'statuses': ['Closed', 'Done', ],
        'style': 'lime-green',
    }),
])


def get_releases(client):
    jira = JIRA(client.url, basic_auth=(client.username, client.get_password()))

    for project in jira.projects():
        clear_query = Release.objects.filter(client=client).filter(project=project.key)
        existing_versions = []
        for version in jira.project_versions(project):
            if version.archived or version.released:
                continue
            existing_versions.append(version.name)

            release = (Release.objects.filter(client=client)
                              .filter(project=project.key)
                              .filter(version=version.name)).first()

            if not release:
                release = Release()
                print(project.key, version.name)
                release.project = project.key
                release.version = version.name
                release.client = client
                release.save()

            release.statuses.all().delete()

            issues = jira.search_issues("project=%s AND fixVersion=%s" % (version.projectId, version.id))
            for key, value in STATUSES.items():
                statuses = value['statuses']
                found_issues = [issue for issue in issues if issue.fields.status.name in statuses]

                release_status = ReleaseStatus()
                release_status.release = release
                release_status.status = key
                release_status.style = value['style']
                release_status.count = len(found_issues)
                release_status.save()
        clear_query.exclude(version__in=existing_versions).all().delete()
