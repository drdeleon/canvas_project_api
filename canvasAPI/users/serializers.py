from rest_framework import serializers

from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_assistant = serializers.SerializerMethodField()
    is_student = serializers.SerializerMethodField()
    is_professor = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'is_assistant',
            'is_student',
            'is_professor',
        )

    def save(self):
        user = User.objects.create_user(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
    def get_is_professor(self, obj):
        return hasattr(obj, 'professor')
    
    def get_is_student(self, obj):
        return hasattr(obj, 'student')
    
    def get_is_assistant(self, obj):
        return hasattr(obj, 'assistant')