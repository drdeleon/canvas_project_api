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
            permission_configuration = {
                'base': {
                    'create': False, # Can only create announcements through courses.
                    'list': True,
                },
                'instance': {
                    'retrieve': 'announcements.view_announcement',
                    'destroy': 'announcements.delete_announcement',
                    'update': 'announcements.change_announcement',
                    'partial_update': 'announcements.change_announcement',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        announcement = serializer.save()
        user = self.request.user
        
        return Response(serializer.data)

