from rest_framework import serializers

from course.models import Course

class CourseSerializers(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'name',
            'section',
            'year',
            'cicle'     
        )