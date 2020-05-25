from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from courses.models import Course
from courses.serializers import CourseSerializer
from announcements.serializers import AnnouncementSerializer
from assignments.serializers import AssignmentSerializer
from groups.serializers import GroupSerializer

from permissions.services import APIPermissionClassFactory

# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='CoursePermission',
            permission_configuration={
                'base': {
                    'create': lambda user, req: user.is_authenticated, # TODO: Debería haber un superusuario
                },
                'instance': {
                    'retrieve': lambda user, req: user.is_authenticated, # TODO: Personas relacionadas con el curso.
                    'destroy': False,
                    'update': 'courses.change_course',
                    'partial_update': 'courses.change_course',
                    'students': lambda user, req: user.is_authenticated, # TODO: Definir permisos
                    'assignments': lambda user, req: user.is_authenticated, # TODO: Definir permisos
                    'announcements': lambda user, req: user.is_authenticated, # TODO: Definir permisos
                    'groups': lambda user, req: user.is_authenticated, # TODO: Definir permisos
                }
            }
        ),
    )

    def perform_create(self, serializer):
        course = serializer.save()
        user = self.request.user
        assign_perm('courses.change_course', user, course)
        assign_perm('courses.view_course', user, course)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        queryset = course.enrollment_set.all().values('student')
        students = CourseSerializer(queryset, many=True).data
        return Response(students)

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        course = self.get_object()
        queryset = course.assignment_set.all().values('student')
        assignments = AssignmentSerializer(queryset, many=True).data
        return Response(assignments)

    @action(detail=True, methods=['get'])
    def announcements(self, request, pk=None):
        course = self.get_object()
        queryset = course.announcement_set.all().values('student')
        announcements = AnnouncementSerializer(queryset, many=True).data
        return Response(announcements)

    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        course = self.get_object()
        queryset = course.group_set.all().values('student')
        groups = GroupSerializer(queryset, many=True).data
        return Response(groups)


