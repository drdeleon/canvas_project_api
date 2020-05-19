from rest_framework import serializers

from assignment.models import Assignment

class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = (
            'title',
            'description',
            'grade',
            'deadline',
            'submission_file'
        )