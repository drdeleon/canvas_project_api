from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from assignments.models import Assignment
from assignments.serializers import AssignmentSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='AssignmentPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'assignments.view_event',
                    'destroy': False,
                    'update': 'assignments.change_event',
                    'partial_update': 'assignments.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('assignments.change_event', user, event)
        assign_perm('assignments.view_event', user, event)
        return Response(serializer.data)