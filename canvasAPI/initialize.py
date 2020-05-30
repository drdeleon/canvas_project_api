from datetime import date

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm, remove_perm

from courses.models import Course
from announcements.models import Announcement
from assignments.models import Assignment
from assistants.models import Assistant
from enrollments.models import Enrollment
from establishments.models import Establishment
from groups.models import Group
from professors.models import Professor
from students.models import Student

# professors = Group.objects.create(name='professors')
# students = Group.objects.create(name='students')
# assistants = Group.objects.create(name='assistants')
user_professor = User.objects.create_user(
    username='user_professor',
    email='user_professor@user.com',
    password='secret'
)
user_student = User.objects.create_user(
    username='user_student',
    email='user_student@user.com',
    password='secret'
)
user_assistant = User.objects.create_user(
    username='user_assistant',
    email='user_assistant@user.com',
    password='secret'
)

# PROFESSOR_TEST
professor = Professor(
    name=user_professor.username,
    user=user_professor
)
professor.save()

# STUDENT_TEST
student = Student(
    name=user_student.username,
    user=user_student
)
student.save()

#ESTABLISHMENT_TEST
establishment = Establishment(
    name='Establishment Test',
    location='Establishment Test Location',
)
establishment.save()

# COURSE_TEST
course = Course(
    establishment=establishment,
    name='course',
    professor=professor,
    section=1,
    year=2000,
    cicle=1,
)
course.save()

# ENROLLMENT_TEST
enrollment = Enrollment(
    student=student,
    course=course,
)
enrollment.save()

# ANNOUNCEMENT_TEST
announcement = Announcement(
    title='Test Announcement Title',
    body='Announcement Test Body',
    course=course,
)
announcement.save()

# ASSIGNMENT_TEST
assignment = Assignment(
    title='Assignment Test Title',
    description='Assignment Test Description',
    score=100.00,
    deadline=date.today(),
    assignment_file='',
    course=course,
    student=student,
)
assignment.save()

# GROUP_TEST
group = Group(
    name = 'Group Test',
    course = course,
)
group.save()
group.students.add(student)

# ASSISTANT_TEST
assistant = Assistant(
    name=user_assistant.username,
    user=user_assistant
)
assistant.save()
assistant.courses.add(course)
