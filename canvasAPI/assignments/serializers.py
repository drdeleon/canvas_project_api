from rest_framework import serializers

from assignments.models import Assignment

class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = (
            "id", 
            "title", 
            "description", 
            "score", 
            "deadline", 
            "assignment_file", 
            "course", 
        )