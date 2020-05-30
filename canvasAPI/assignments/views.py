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
                    'create': False,
                },
                'instance': {
                    'retrieve': 'assignments.view_assignment',
                    'destroy': False,
                    'update': 'assignments.change_assignment',
                    'partial_update': 'assignments.change_assignment',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        assignment = serializer.save()
        user = self.request.user

        # Assign student perms(view, change)
        assign_perm('assignments.change_assignment', assignment.student.user, assignment)
        assign_perm('assignments.view_assignment', assignment.student.user, assignment)

        # Assign professor perms(view, change)
        assign_perm('assignments.change_assignment', assignment.course.professor.user, assignment)
        assign_perm('assignments.view_assignment', assignment.course.professor.user, assignment)

        # Assign assistant perms(view, change)
        for assistant in assignment.course.assistant_set.all():
            assign_perm('assignments.change_assignment', assistant.user, assignment)
            assign_perm('assignments.view_assignment', assistant.user, assignment)

        return Response(serializer.data)