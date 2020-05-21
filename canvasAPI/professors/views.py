from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from professors.models import Professor
from professors.serializers import ProfessorSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='ProfessorPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'professors.view_event',
                    'destroy': False,
                    'update': 'professors.change_event',
                    'partial_update': 'professors.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('professors.change_event', user, event)
        assign_perm('professors.view_event', user, event)
        return Response(serializer.data)