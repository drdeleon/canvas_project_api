from rest_framework import serializers

from submission_files.models import SubmissionFile

class SubmissionFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubmissionFile
        fields = (
            'id',
            'title'
        )