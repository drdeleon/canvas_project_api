from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=300)
    ##  campo user

    def __str__(self):
        return 'Student: {}'.format(slef.name)