from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from enrollments.models import Enrollment
from enrollments.serializers import EnrollmentSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='EnrollmentPermission',
            permission_configuration = {
                'base': {
                    'create': lambda user, req: user.is_authenticated, # TODO: Debería se un superusuario.
                },
                'instance': {
                    'retrieve': lambda user, req: user.is_authenticated, # TODO: Personal autorizado.
                    'destroy': False,
                    'update': 'enrollments.change_enrollment',
                    'partial_update': 'enrollments.change_enrollment',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        enrollment = serializer.save()
        user = self.request.user
        assign_perm('enrollments.change_enrollment', user, enrollment)
        assign_perm('enrollments.view_enrollment', user, enrollment)
        return Response(serializer.data)