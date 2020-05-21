from django.db import models

# Create your models here.
class Establishment(models.Model):
    name = models.CharField(max_length=300)
    location = models.CharField(max_length=300)

    def __str__(self):
        return 'Establishment: {}'.format(self.name)
