from rest_framework import serializers

from professor.models import Professor

class ProfessorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Professor
        fields = (
            'name'
        )