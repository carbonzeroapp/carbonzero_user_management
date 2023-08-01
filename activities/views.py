from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from activities.models import Activity
from activities.serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
