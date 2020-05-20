from django.db import models

# Create your models here.
class Course(models.Model):
    ##  agregar campo de establishment
    stablishment = models.ForeignKey("stablishments.Stablishment", on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    professor = models.ForeignKey("professors.Professor", on_delete=models.SET_NULL)
    section = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    cicle = models.PositiveIntegerField()

    def __str__(self):
        return 'Course: {}'.format(self.name)