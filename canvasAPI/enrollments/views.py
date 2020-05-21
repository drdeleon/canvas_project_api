from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from enrollments.models import Enrollment
from enrollments.serializers import EnrollmentSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='EnrollmentPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'enrollments.view_event',
                    'destroy': False,
                    'update': 'enrollments.change_event',
                    'partial_update': 'enrollments.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('enrollments.change_event', user, event)
        assign_perm('enrollments.view_event', user, event)
        return Response(serializer.data)