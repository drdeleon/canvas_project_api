from django.db import models

# Create your models here.
class Professor(models.Model):
    name = models.CharField(max_length=300)
    ##  campo user

    def __str__(self):
        return 'Professor: {}'.format(self.name)