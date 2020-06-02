from rest_framework import serializers

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    assistant = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    professor = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'assistant',
            'student',
            'professor',
        )

    def save(self):
        user = User.objects.create_user(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
    def get_professor(self, obj):
        if(hasattr(obj, 'professor')):
            return obj.professor.id
        return False
    
    def get_student(self, obj):
        if(hasattr(obj, 'student')):
            return obj.student.id
        return False
    
    def get_assistant(self, obj):
        if(hasattr(obj, 'assistant')):
            return obj.assistant.id
        return False