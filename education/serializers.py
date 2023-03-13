from django.conf import settings
from rest_framework import serializers

from education.models import Course, Lesson, Subscription, Payments
from education.validators import LessonValidator


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        validators = [LessonValidator(field='video_url')]
        fields = (
            'id',
            'title',
            'description',
            'video_url'
        )


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True)
    subs_status = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'price',
            'lesson',
            'lesson_count',
            'subs_status'
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

    def get_subs_status(self, instance):
        user = self.context['request'].user.id
        obj = Payments.objects.filter(course=instance).filter(user=user)
        if obj:
            return obj.first().subscription_set.first().status
        return False


class PaymentsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(default=serializers.CurrentUserDefault())
    subs_status = serializers.SerializerMethodField()

    class Meta:
        model = Payments
        fields = '__all__'

    def create(self, validated_data):
        new_payment = Payments.objects.create(**validated_data)
        Subscription.objects.create(payment=new_payment)
        return new_payment

    def get_subs_status(self, instance):
        if subscription := Subscription.objects.filter(payment=instance):
            return subscription.first().status
        else:
            return None