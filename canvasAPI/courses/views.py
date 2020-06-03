from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from courses.models import Course
from groups.models import Group
from students.models import Student
from enrollments.models import Enrollment
from assistants.models import Assistant
from assignments.models import Assignment
from announcements.models import Announcement

from courses.serializers import CourseSerializer
from announcements.serializers import AnnouncementSerializer
from assignments.serializers import AssignmentSerializer
from groups.serializers import GroupSerializer
from students.serializers import StudentSerializer
from enrollments.serializers import EnrollmentSerializer
from assistants.serializers import AssistantSerializer

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
                    'create': True, # TODO: Debería haber un superusuario
                    'list': True
                },
                'instance': {
                    'retrieve': 'courses.view_course',
                    'destroy': False,
                    'update': 'courses.change_course',
                    'partial_update': 'courses.change_course',
                    'students': 'courses.view_course',
                    'assistants': 'courses.view_course',
                    'assignments': 'courses.view_course',
                    'announcements': 'courses.view_course',
                    'groups': 'courses.view_course',
                    'enrollments': 'courses.view_course',
                    'create_course_group': 'courses.change_course',
                    'create_course_announcement': 'courses.change_course',
                    'add_student': 'courses.change_course',
                    'remove_student': 'courses.change_course',
                    'add_assistant': 'courses.change_course',
                    'remove_assistant': 'courses.change_course',
                    'create_course_assignment': 'courses.change_course',
                    'delete_course_assignment': 'courses.change_course',
                    'update_course_assignment': 'courses.change_course',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        course = serializer.save()
        # Assign view permission for every student in the course.
        for enr in course.enrollment_set.all():
            assign_perm('courses.view_course', enr.student.user, course)

        # Assign assistants' perms (view)
        for assistant in course.assistant_set.all():
            assign_perm('courses.view_course', assistant.user, course)

        # Assign professor's perms (change, view)
        assign_perm('courses.change_course', course.professor.user, course)
        assign_perm('courses.view_course', course.professor.user, course)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        # Obtain course's students from enrollments.
        students = [] 
        for enr in course.enrollment_set.all():
            students.append(enr.student)
        students = StudentSerializer(students, many=True).data
        return Response(students)

    @action(detail=True, methods=['get'])
    def assistants(self, request, pk=None):
        course = self.get_object()
        # Obtain course's assistants from enrollments.
        assistants = [] 
        for assistant in course.assistant_set.all():
            assistants.append(assistant)
        assistants = AssistantSerializer(assistants, many=True).data
        return Response(assistants)

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        course = self.get_object()
        queryset = course.assignment_set.all()
        assignments = AssignmentSerializer(queryset, many=True).data
        return Response(assignments)

    @action(detail=True, methods=['get'])
    def announcements(self, request, pk=None):
        course = self.get_object()
        queryset = course.announcement_set.all()
        announcements = AnnouncementSerializer(queryset, many=True).data
        return Response(announcements)

    @action(detail=True, methods=['get'])
    def groups(self, request, pk=None):
        course = self.get_object()
        queryset = course.group_set.all()
        groups = GroupSerializer(queryset, many=True).data
        return Response(groups)

    @action(detail=True, methods=['get'])
    def enrollments(self, request, pk=None):
        course = self.get_object()
        queryset = course.enrollment_set.all()
        enrollments = EnrollmentSerializer(queryset, many=True).data
        return Response(enrollments)

    @action(detail=True,url_path='create-group', methods=['post'])
    def create_course_group(self, request, pk=None):
        course = self.get_object()
        group_name  = request.data.get('name')
        group = Group(name=group_name, course=course)
        group.save()
        for student in group.students.all():
            assign_perm('groups.view_group', student.user, group)

        # Assign view permission to students in group
        for assistant in group.course.assistant_set.all():
            assign_perm('groups.view_group', assistant.user, group)
            assign_perm('groups.change_group', assistant.user, group)

        assign_perm('groups.change_group', group.course.professor.user, group)
        assign_perm('groups.delete_group', group.course.professor.user, group)
        assign_perm('groups.view_group', group.course.professor.user, group)
        return Response(GroupSerializer(group).data)

    @action(detail=True,url_path='create-announcement', methods=['post'])
    def create_course_announcement(self, request, pk=None):
        course = self.get_object()
        announcement_title  = request.data.get('title')
        announcement_body  = request.data.get('body')
        announcement = Announcement(title=announcement_title, body=announcement_body, course=course)
        announcement.save()
        return Response(AnnouncementSerializer(announcement).data)

    @action(detail=True,url_path='add-student', methods=['post'])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id  = request.data.get('student')
        student = Student.objects.get(pk=student_id)
        enrollment = Enrollment(course=course, student=student)
        enrollment.save()
        # Assign perm to view course
        assign_perm('courses.view_course', student.user, course)
        return Response(EnrollmentSerializer(enrollment).data)

    @action(detail=True,url_path='remove-student', methods=['post'])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id  = request.data.get('student')
        student = Student.objects.get(pk=student_id)
        enrollment = course.enrollment_set.get(student)
        enrollment.delete()
        # Unassign perm to view course
        remove_perm('courses.view_course', student.user, course)

        return Response(EnrollmentSerializer(enrollment).data)

    @action(detail=True,url_path='add-assistant', methods=['post'])
    def add_assistant(self, request, pk=None):
        course = self.get_object()
        assistant_id  = request.data.get('assistant')
        assistant = Assistant.objects.get(pk=assistant_id)
        course.assistant_set.add(assistant)
        # Assign perm to view course
        assign_perm('courses.view_course', assistant.user, course)

        return Response(AssistantSerializer(assistant).data)

    @action(detail=True,url_path='remove-assistant', methods=['post'])
    def remove_assistant(self, request, pk=None):
        course = self.get_object()
        assistant_id  = request.data.get('assistant')
        assistant = Assistant.objects.get(pk=assistant_id)
        course.assistant_set.remove(assistant)
        # Unassign perm to view course
        remove_perm('courses.view_course', assistant.user, course)

        return Response(AssistantSerializer(assistant).data)

    @action(detail=True,url_path='create-assignment', methods=['post'])
    def create_course_assignment(self, request, pk=None):
        course = self.get_object()
        for enrollment in course.enrollment_set.all():
            assignment = enrollment.student.assignment_set.create(
                title = request.data.get('title'),
                description = request.data.get('description'),
                deadline = request.data.get('deadline'),
                assignment_file = request.data.get('assignment_file'),
                course = course)
        return Response(AssignmentSerializer(assignment).data)

    @action(detail=True,url_path='delete-assignment', methods=['post'])
    def delete_course_assignment(self, request, pk=None):
        course = self.get_object()
        title = request.data.get('title')
        # Buscar assignments por título
        # TODO: Filtrar por fecha de creación
        for assignment in Assignment.objects.filter(title=title, course=course).all():
            assignment.delete()
        return Response(AssignmentSerializer(assignment).data)

    @action(detail=True,url_path='update-assignment', methods=['post'])
    def update_course_assignment(self, request, pk=None):
        course = self.get_object()
        title = request.data.get('title')
        # Buscar assignments por título
        # TODO: Filtrar por fecha de creación
        Assignment.objects.filter(title=title, course=course).update(
            title = request.data.get('title'),
            description = request.data.get('description'),
            score = request.data.get('score'),
            deadline = request.data.get('deadline'),
            assignment_file = request.data.get('assignment_file'),
            course = request.data.get('course'))
        for assignment in Assignment.objects.filter(title=title, course=course).all():
            assignment.save()
        return Response(AssignmentSerializer(assignment).data)




