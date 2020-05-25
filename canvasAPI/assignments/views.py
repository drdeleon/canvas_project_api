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
                    'create': lambda user, req: user.is_authenticated, # TODO: Solo si es profesor del curso
                    # 'list': False,
                },
                'instance': {
                    'retrieve': lambda user, req: user.is_authenticated, # TODO: Solo si tiene acceso al curso
                    'destroy': 'assignments.delete_assignment',
                    'update': 'assignments.change_assignment',
                    'partial_update': 'assignments.change_assignment',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        assignment = serializer.save()
        user = self.request.user

        #Agregar el assignment a cada estudiante en el curso
        for student in assignment.course.student_set.all():
            student.assignments.add(assignment)

        assign_perm('assignments.change_assignment', user, assignment)
        assign_perm('assignments.delete_assignment', user, assignment)
        return Response(serializer.data)