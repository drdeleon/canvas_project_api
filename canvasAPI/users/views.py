from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from users.serializers import UserRegistrationSerializer


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Usuario registrado con éxito'
            data['username'] = user.username
            data['email'] = user.email
        else:
            data = serializer.errors
        
        return Response(data)

