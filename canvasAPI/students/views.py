from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm
from permissions.services import APIPermissionClassFactory

from students.models import Student
from students.serializers import StudentSerializer
from enrollments.serializers import EnrollmentSerializer
from courses.serializers import CourseSerializer
from assignments.serializers import AssignmentSerializer
from groups.serializers import GroupSerializer


def get_student_courses(self, student):
    courses = student.enrollment_set.all().values('course')
    print('courses:', courses)
    return courses

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='StudentPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    # 'list': False,
                },
                'instance': {
                    'retrieve': 'students.view_student',
                    'destroy': False,
                    'update': 'students.change_student',
                    'partial_update': 'students.change_student',
                    'enrollments': 'students.view_student',
                    'assignments': 'students.view_student',
                    'groups': 'students.view_student',
                    'courses': 'students.view_student',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        student = serializer.save()
        user = self.request.user
        assign_perm('students.change_student', user, student)
        assign_perm('students.view_student', user, student)
        return Response(serializer.data)

    # Get student's enrollments.
    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        student = self.get_object()
        queryset = student.enrollment_set.all()
        enrollments = EnrollmentSerializer(queryset, many=True).data
        return Response(enrollments)

    # Get student's assignments.
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        student = self.get_object()
        queryset = student.assignment_set.all()
        assignments = AssignmentSerializer(queryset, many=True).data
        return Response(assignments)

    # Get stududent's groups.
    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        student = self.get_object()
        queryset = student.group_set.all()
        groups = GroupSerializer(queryset, many=True).data
        return Response(groups)

    # Get student's courses.
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        student = self.get_object()
        courses = self.get_student_courses(student)
        courses = CourseSerializer(courses, many=True).data
        return Response(courses)

