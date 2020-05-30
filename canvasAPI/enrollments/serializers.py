from rest_framework import serializers

from enrollments.models import Enrollment

class EnrollmentSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Enrollment
        fields = ( 
            'id',
            'course',
            'student',
            'data'
        )