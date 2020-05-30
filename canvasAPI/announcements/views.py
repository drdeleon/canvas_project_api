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
                    # 'list': False,
                },
                'instance': {
                    'retrieve': 'annoucements.view_announcement',
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
        # Assign professor perms (view, change, delete)
        assign_perm('announcements.view_announcement', announcement.course.professor.user, announcement)
        assign_perm('announcements.change_announcement', announcement.course.professor.user, announcement)
        assign_perm('announcements.delete_announcement', announcement.course.professor.user, announcement)
        # Assign assitants' perms (view, change)
        for assistant in announcement.course.assistant_set.all():
            assign_perm('announcements.view_announcement', assistant.user, announcement)
            assign_perm('announcements.change_announcement', assistant.user, announcement)

        # Assign student perms (view)
        for enrollment in announcement.course.enrollment_set.all():
            assign_perm('announcements.view_announcement', enrollment.student.user, announcement)

        # assign_perm('announcements.change_announcement', user, announcement)
        # assign_perm('announcements.delete_announcement', user, announcement)
        return Response(serializer.data)