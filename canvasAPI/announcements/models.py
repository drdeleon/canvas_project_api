from django.db import models

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=300)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )