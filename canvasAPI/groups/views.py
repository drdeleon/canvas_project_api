from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from groups.models import Group
from students.models import Student
from groups.serializers import GroupSerializer
from permissions.services import APIPermissionClassFactory

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='GroupPermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated, # TODO: Solo si está relacionado.
                    # 'list': lambda user, req: user.is_authenticated,
                },
                'instance': {
                    'retrieve': lambda user, req: user.is_authenticated, # TODO: Si está relacionado.
                    'destroy': False,
                    'update': 'groups.change_group',
                    'partial_update': 'groups.change_group',
                    'add_student': True,
                }
            }
        ),
    )

    def perform_create(self, serializer):
        group = serializer.save()
        user = self.request.user
        assign_perm('groups.change_group', user, group)
        assign_perm('groups.view_group', user, group)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def add_student(self, request, pk=None):
        group = self.get_object()
        student_id = request.data.get('student')
        student = Student.objects.get(id=student_id)
        group.students.add(student)
        group.save()
        return Response(GroupSerializer(group).data)

        
