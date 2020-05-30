from django.db import models

# Create your models here.
class Enrollment(models.Model):
    course = models.ForeignKey(
        "courses.Course", 
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        "students.Student", 
        on_delete=models.CASCADE
    )
    date = models.DateField(auto_now_add=True, auto_now=False, null=True)