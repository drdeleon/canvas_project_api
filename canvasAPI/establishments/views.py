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
                    'create': lambda user, req: user.is_authenticated, # TODO: Debería ser solo superuser.
                },
                'instance': {
                    'retrieve': lambda user, req: user.is_authenticated, # TODO: Solo si está relacionado.
                    'destroy': False,
                    'update': 'establishments.change_establishment',
                    'partial_update': 'establishments.change_establishment',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        establishment = serializer.save()
        user = self.request.user
        assign_perm('establishments.change_establishment', user, establishment)
        return Response(serializer.data)