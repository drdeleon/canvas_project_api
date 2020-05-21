from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from establishments.models import Establishment
from establishments.serializers import EstablishmentSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class EstablishmentViewSet(viewsets.ModelViewSet):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='EstablishmentPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'establishments.view_event',
                    'destroy': False,
                    'update': 'establishments.change_event',
                    'partial_update': 'establishments.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('establishments.change_event', user, event)
        assign_perm('establishments.view_event', user, event)
        return Response(serializer.data)