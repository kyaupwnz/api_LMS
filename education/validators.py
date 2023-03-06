from rest_framework import serializers


class LessonValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if 'youtube' not in value.get('video_url'):
            raise serializers.ValidationError('Возможны ссылки только на youtube.com')
