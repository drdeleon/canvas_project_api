from django.db import models

# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    grade = models.FloatField()
    deadline = models.DateField()
    ##  agregar campo para archivo

    def __str__(self):
        return 'Assignment: {}'.format(self.title)