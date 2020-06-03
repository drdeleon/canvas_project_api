from django.db import models
from guardian.shortcuts import assign_perm, remove_perm

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

    def save(self, *args, **kwargs):
        group = self
        super().save(*args, **kwargs)
        
        # Assign view permission to students in group
        for student in group.students.all():
            assign_perm('groups.view_group', student.user, group)

        # Assign view permission to students in group
        for assistant in group.course.assistant_set.all():
            assign_perm('groups.view_group', assistant.user, group)
            assign_perm('groups.change_group', assistant.user, group)

        assign_perm('groups.change_group', group.course.professor.user, group)
        assign_perm('groups.delete_group', group.course.professor.user, group)
        assign_perm('groups.view_group', group.course.professor.user, group)