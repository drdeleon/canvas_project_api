from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from groups.models import Group
from groups.serializers import GroupSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='GroupPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'groups.view_event',
                    'destroy': False,
                    'update': 'groups.change_event',
                    'partial_update': 'groups.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('groups.change_event', user, event)
        assign_perm('groups.view_event', user, event)
        return Response(serializer.data)