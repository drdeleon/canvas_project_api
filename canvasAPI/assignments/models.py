from django.db import models

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/assignments/{1}'.format(instance.user.id, filename)

# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500, blank=True)
    score = models.FloatField(blank=True)
    deadline = models.DateField()
    assignment_file = models.FileField(upload_to=user_directory_path, max_length=100, blank=True)
    course = models.ForeignKey("courses.Course",null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Assignment: {}'.format(self.title)