from jira import JIRA

from ..models.sprint import SprintIssue, SprintIssueAssignee, SprintIssueType


# TODO user should configure that
STATUSES = {
    # Open
    'Open': 'Open',
    'Backlog': 'Open',
    'Selected for Development': 'Open',

    # WIP
    'In Progress': "WIP",
    'Waiting Pull Request': "WIP",

    # Review
    'Code Revision': "Review",

    # Validation
    'To Test': "Validation",
    'Testing': "Validation",

    # Test
    'Closed': "Done",
    'Done': "Done",
}


def get_sprint_issues(client):
    jira = JIRA(client.url, basic_auth=(client.username, client.get_password()))

    issues = jira.search_issues("Sprint in openSprints() order by rank")
    clear_query = SprintIssue.objects.filter(client=client)
    existing_keys = []
    for issue in issues:
        existing_keys.append(issue.key)
        sprint_issue = (SprintIssue.objects.filter(key=issue.key)).first()

        if not sprint_issue:
            sprint_issue = SprintIssue()
            sprint_issue.key = issue.key

        assignee = None
        if issue.fields.assignee:
            assignee = SprintIssueAssignee.objects.create_or_update(
                display_name=issue.fields.assignee.displayName,
                avatar=getattr(issue.fields.assignee.avatarUrls, "48x48"),
                email=issue.fields.assignee.emailAddress,
            )

        issue_type = SprintIssueType.objects.create_or_update(
            name=issue.fields.issuetype.name,
            icon=issue.fields.issuetype.iconUrl,
        )

        # customfield_10200 is rank
        sprint_issue.url = issue.permalink()
        sprint_issue.rank = issue.fields.customfield_10200
        sprint_issue.issue_type = issue_type
        sprint_issue.project = issue.fields.project.name
        sprint_issue.status = STATUSES.get(issue.fields.status.name, issue.fields.status.name)
        sprint_issue.assignee = assignee
        sprint_issue.client = client
        sprint_issue.save()
    clear_query.exclude(key__in=existing_keys).all().delete()
