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
                    'create': False,
                },
                'instance': {
                    'retrieve': 'assignments.view_assignment',
                    'destroy': False,
                    'update': 'assignments.change_assignment',
                    'partial_update': 'assignments.change_assignment',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        assignment = serializer.save()
        user = self.request.user

        return Response(serializer.data)