from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from education.models import Course, Lesson, Payments, Subscription
from education.permissions import IsManager, IsModerator
from education.serializers import CourseSerializer, LessonSerializer, PaymentsSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsManager]
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
        if self.action == 'update':
            permission_classes = [IsManager | IsModerator]
        if self.action == 'partial_update':
            permission_classes = [IsManager | IsModerator]
        if self.action == 'destroy':
            permission_classes = [IsManager]
        return [permission() for permission in permission_classes]

    # def get_queryset(self):
    #     if self.request.user.has_perm('education.view_course'):
    #         return Course.objects.all()
    #     else:
    #         paid_courses = self.request.user.payments_set.values_list('course_id')
    #         return Course.objects.filter(pk__in=paid_courses)


class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsManager | IsModerator | IsAuthenticated]

    def get_queryset(self):
        if self.request.user.has_perm('education.view_lesson'):
            return Lesson.objects.all()
        else:
            paid_lessons = self.request.user.payments_set.values_list('lesson_id')
            return Lesson.objects.filter(pk__in=paid_lessons)


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager]


class LessonRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsManager | IsModerator | IsAuthenticated]

    def get_queryset(self):
        if self.request.user.has_perm('education.view_lesson'):
            return Lesson.objects.all()
        else:
            paid_lessons = self.request.user.payments_set.values_list('lesson_id')
            return Lesson.objects.filter(pk__in=paid_lessons)


class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager | IsModerator]


class LessonDestroyApiView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsManager]


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsCreateApiView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentsUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated, IsModerator, IsManager]

    def perform_update(self, serializer):
        obj = Payments.objects.get(pk=self.kwargs.get('pk'))
        sub = Subscription.objects.get(payment_id=obj)
        if sub.status:
            sub.status = False
            sub.save()
        else:
            sub.status = True
            sub.save()


class PaymentsDestroyApiView(generics.DestroyAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsManager]

