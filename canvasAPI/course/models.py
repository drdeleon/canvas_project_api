from django.db import models

# Create your models here.
class Course(models.Model):
    ##  agregar campo de establishment
    name = models.CharField(max_length=300)
    ##  agregar campo de professor
    section = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    cicle = models.PositiveIntegerField()

    def __str__(self):
        return 'Course: {}'.format(self.name)