from django.db import models

# Create your models here.
class Course(models.Model):
    establishment = models.ForeignKey(
        "establishments.Establishment", 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    name = models.CharField(max_length=300)
    professor = models.ForeignKey(
        "professors.Professor", 
        null=True, 
        on_delete=models.SET_NULL
    )
    section = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    cicle = models.PositiveIntegerField()

    def __str__(self):
        return 'Course: {}'.format(self.name)