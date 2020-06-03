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
                    'create': False, # Lógica que se maneja en curso.
                    # 'list': True
                },
                'instance': {
                    'retrieve': 'groups.view_group', # TODO: Estudiantes, Auxiliares y Profesor.
                    'destroy': 'groups.delete_group',
                    'update': 'groups.change_group',
                    'partial_update': 'groups.change_group',
                    'add_student': 'groups.change_group',
                    'remove_student': 'groups.change_group',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        group = serializer.save()
        user = self.request.user

        return Response(serializer.data)

    @action(detail=True, url_path='add-student', methods=['post'])
    def add_student(self, request, pk=None):
        group = self.get_object()
        student_id = request.data.get('student')
        student = Student.objects.get(id=student_id)
        group.students.add(student)
        assign_perm('groups.view_group', student.user, group)
        group.save()
        return Response(GroupSerializer(group).data)

    @action(detail=True, url_path='remove-student', methods=['post'])
    def remove_student(self, request, pk=None):
        group = self.get_object()
        student_id = request.data.get('student')
        student = Student.objects.get(id=student_id)
        group.students.remove(student)
        remove_perm('groups.view_group', student.user, group)
        group.save()
        return Response(GroupSerializer(group).data)

        
