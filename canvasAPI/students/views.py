from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from students.models import Student
from students.serializers import StudentSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='StudentPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'students.view_event',
                    'destroy': False,
                    'update': 'students.change_event',
                    'partial_update': 'students.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('students.change_event', user, event)
        assign_perm('students.view_event', user, event)
        return Response(serializer.data)