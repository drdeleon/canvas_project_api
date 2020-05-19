from rest_framework import serializers

from announcement.mododels import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = (
            'title',
            'body',
            'course'
        )