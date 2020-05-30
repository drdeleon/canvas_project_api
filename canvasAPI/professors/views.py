from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm
from permissions.services import APIPermissionClassFactory

from professors.models import Professor

from professors.serializers import ProfessorSerializer
from courses.serializers import CourseSerializer

# Create your views here.
class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='ProfessorPermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'professors.view_professor',
                    'destroy': False,
                    'update': 'professors.change_professor',
                    'partial_update': 'professors.change_professor',
                    'courses': 'professors.view_professor'
                }
            }
        ),
    )

    def perform_create(self, serializer):
        professor = serializer.save()
        user = self.request.user
        assign_perm('professors.change_professor', user, professor)
        assign_perm('professors.view_professor', user, professor)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        professor = self.get_object()
        queryset = professor.course_set.all()
        courses = CourseSerializer(queryset, many=True).data
        return Response(courses)