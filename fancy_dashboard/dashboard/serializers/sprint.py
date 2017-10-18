from fancy_dashboard.dashboard.models.sprint import SprintIssue
from fancy_dashboard.dashboard.models.sprint import SprintIssueAssignee
from fancy_dashboard.dashboard.models.sprint import SprintIssueType
from rest_framework import serializers


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprintIssueAssignee
        fields = ('display_name', 'email', 'avatar')


class IssueTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SprintIssueType
        fields = ('name', 'icon')


class SprintSerializer(serializers.ModelSerializer):
    many = True

    assignee = AssigneeSerializer()
    issue_type = IssueTypeSerializer()

    class Meta:
        model = SprintIssue
        fields = ('rank', 'url', 'key', 'assignee', 'issue_type', 'project', 'status')
