from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from users.serializers import UserSerializer

from guardian.shortcuts import assign_perm
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from permissions.services import APIPermissionClassFactory
from django.contrib.auth.models import User


DAYS_IN_YEAR = 365

def evaluar_user(user, obj, request):
    return user == obj


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        APIPermissionClassFactory(
            name='UserPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    'list': True
                },
                'instance': {
                    'retrieve': evaluar_user,
                    'destroy': False,
                    'update': evaluar_user,
                    'partial_update': evaluar_user,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        user = serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Usuario registrado con éxito'
            data['username'] = user.username
            data['email'] = user.email
        else:
            data = serializer.errors
        
        return Response(data)

