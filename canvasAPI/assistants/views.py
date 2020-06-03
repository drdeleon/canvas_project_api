from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm
from permissions.services import APIPermissionClassFactory

from assistants.models import Assistant

from assistants.serializers import AssistantSerializer
from courses.serializers import CourseSerializer

# Create your views here.
class AssistantViewSet(viewsets.ModelViewSet):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='AssistantPermission',
            permission_configuration={
                'base': {
                    'create': True,
                    # 'list': True
                },
                'instance': {
                    'retrieve': 'assistants.view_assistant',
                    'destroy': False,
                    'update': 'assistants.change_assistant',
                    'partial_update': 'assistants.change_assistant',
                    'courses': 'assistants.view_assistant',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        assistant = serializer.save()
        user = self.request.user
        assistant.user = user 
        assistant.save()
        assign_perm('assistants.change_assistant', user, assistant)
        assign_perm('assistants.view_assistant', user, assistant)
        return Response(serializer.data)

    # Get assistant's courses.
    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        assistant = self.get_object()
        courses = assistant.courses.all()
        courses = CourseSerializer(courses, many=True).data
        return Response(courses)