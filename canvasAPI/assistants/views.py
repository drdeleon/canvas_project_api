from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from assistants.models import Assistant
from assistants.serializers import AssistantSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='AssistantPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'assistants.view_event',
                    'destroy': False,
                    'update': 'assistants.change_event',
                    'partial_update': 'assistants.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('assistants.change_event', user, event)
        assign_perm('assistants.view_event', user, event)
        return Response(serializer.data)