from django.db import models
from datetime import date
from guardian.shortcuts import assign_perm, remove_perm

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/assignments/{1}'.format(instance.user.id, filename)

# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=500,  blank=True)
    score = models.FloatField(blank=True, default=0.0)
    creation_date = models.TimeField(auto_now=True, auto_now_add=False)
    deadline = models.DateField()
    assignment_file = models.FileField(upload_to=user_directory_path, max_length=100, blank=True)
    course = models.ForeignKey("courses.Course", null=True, on_delete=models.SET_NULL)
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        assignment = self
        super().save(*args, **kwargs)
        
        # Assign student perms(view, change)
        assign_perm('assignments.change_assignment', assignment.student.user, assignment)
        assign_perm('assignments.view_assignment', assignment.student.user, assignment)

        # Assign professor perms(view, change)
        assign_perm('assignments.change_assignment', assignment.course.professor.user, assignment)
        assign_perm('assignments.view_assignment', assignment.course.professor.user, assignment)

        # Assign assistant perms(view, change)
        for assistant in assignment.course.assistant_set.all():
            assign_perm('assignments.change_assignment', assistant.user, assignment)
            assign_perm('assignments.view_assignment', assistant.user, assignment)

