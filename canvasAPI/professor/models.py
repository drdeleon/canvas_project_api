from django.db import models

# Create your models here.
class Professor(models.Model):
    name = models.CharField(max_length=300)
    user = models.OneToOneField("models.User", on_delete=models.CASCADE)

    def __str__(self):
        return 'Professor: {}'.format(self.name)