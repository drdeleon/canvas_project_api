from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from announcements.models import Announcement
from announcements.serializers import AnnouncementSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='AnnouncementPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'announcements.view_event',
                    'destroy': False,
                    'update': 'announcements.change_event',
                    'partial_update': 'announcements.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('announcements.change_event', user, event)
        assign_perm('announcements.view_event', user, event)
        return Response(serializer.data)