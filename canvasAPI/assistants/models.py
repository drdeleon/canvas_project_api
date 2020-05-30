from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Assistant(models.Model):
    name = models.CharField(max_length=300)
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
        
    courses = models.ManyToManyField("courses.Course")

    class Meta:
        permissions = (
            ('is_assistant', 'Check if is assistant'),
        )

    def __str__(self):
        return self.name