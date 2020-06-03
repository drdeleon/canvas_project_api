from django.db import models
from guardian.shortcuts import assign_perm, remove_perm

# Create your models here.
class Announcement(models.Model):
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=300)
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    def save(self, *args, **kwargs):
        announcement = self
        super().save(*args, **kwargs)
        
        assign_perm('announcements.view_announcement', announcement.course.professor.user, announcement)
        assign_perm('announcements.change_announcement', announcement.course.professor.user, announcement)
        assign_perm('announcements.delete_announcement', announcement.course.professor.user, announcement)
        # Assign assitants' perms (view, change)
        for assistant in announcement.course.assistant_set.all():
            assign_perm('announcements.view_announcement', assistant.user, announcement)
            assign_perm('announcements.change_announcement', assistant.user, announcement)

        # Assign student perms (view)
        for enrollment in announcement.course.enrollment_set.all():
            assign_perm('announcements.view_announcement', enrollment.student.user, announcement)