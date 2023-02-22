from rest_framework import serializers

from education.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            'id',
            'title',
            'description',
            'video_url'
        )


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'lesson',
            'lesson_count'
        )

    def create(self, validated_data):
        new_lesson = validated_data.pop('lesson_set')
        new_course = Course.objects.create(**validated_data)
        for lesson_data in new_lesson:
            Lesson.objects.get_or_create(course=new_course, **lesson_data)
        return new_course

    def get_lesson_count(self, instance):
        lesson_object = Lesson.objects.filter(course=instance)
        if lesson_object:
            return lesson_object.count()
        return 0
