from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from guardian.shortcuts import assign_perm, remove_perm

from submission_files.models import SubmissionFile
from submission_files.serializers import SubmissionFileSerializer
from permissions.services import APIPermissionClassFactory

# Create your views here.
class SubmissionFileViewSet(viewsets.ModelViewSet):
    queryset = SubmissionFile.objects.all()
    serializer_class = SubmissionFileSerializer

    permission_classes = (
        APIPermissionClassFactory(
            name='SubmissionFilePermission',
            permission_configuration={
                'base': {
                    'create': True,
                },
                'instance': {
                    'retrieve': 'submission_files.view_event',
                    'destroy': False,
                    'update': 'submission_files.change_event',
                    'partial_update': 'submission_files.change_event',
                }
            }
        ),
    )

    def perform_create(self, serializer):
        event = serializer.save()
        user = self.request.user
        assign_perm('submission_files.change_event', user, event)
        assign_perm('submission_files.view_event', user, event)
        return Response(serializer.data)