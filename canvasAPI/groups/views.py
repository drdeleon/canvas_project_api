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

        # Assign view permission to students in group
        for student in group.students.all():
            assign_perm('groups.view_group', student.user, group)

        # Assign view permission to students in group
        for assistant in group.course.assistant_set.all():
            assign_perm('groups.view_group', assistant.user, group)
            assign_perm('groups.change_group', assistant.user, group)

        assign_perm('groups.change_group', group.course.professor.user, group)
        assign_perm('groups.delete_group', group.course.professor.user, group)
        assign_perm('groups.view_group', group.course.professor.user, group)
        # assign_perm('groups.change_group', user, group)
        # assign_perm('groups.view_group', user, group)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        group = self.get_object()
        student_id = request.data.get('student')
        student = Student.objects.get(id=student_id)
        group.students.add(student)
        assign_perm('groups.view_group', student.user, group)
        group.save()
        return Response(GroupSerializer(group).data)

    @action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        group = self.get_object()
        student_id = request.data.get('student')
        student = Student.objects.get(id=student_id)
        group.students.remove(student)
        remove_perm('groups.view_group', student.user, group)
        group.save()
        return Response(GroupSerializer(group).data)

        
