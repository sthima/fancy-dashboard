from rest_framework import viewsets

from ..models.sprint import SprintIssue
from ..serializers.sprint import SprintSerializer


class SprintViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows sprints to be listed.
    """
    queryset = SprintIssue.objects.all().order_by('rank')
    serializer_class = SprintSerializer
