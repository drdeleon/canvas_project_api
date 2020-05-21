from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from courses.models import Course
from courses.serializers import CourseSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='CoursePermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'courses.view_event',
                    'destroy': False,
                    'update': 'courses.change_event',
                    'partial_update': 'courses.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('courses.change_event', user, event)
        assign_perm('courses.view_event', user, event)
        return Response(serializer.data)