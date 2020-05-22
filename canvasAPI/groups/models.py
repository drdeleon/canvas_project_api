from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=300)
    course = models.ForeignKey(
        "courses.Course", 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    students = models.ManyToManyField(
        "students.Student"
    )