from django.urls import path
from rest_framework.routers import DefaultRouter

from education.views import CourseViewSet, LessonListView, LessonCreateApiView, LessonRetrieveApiView, \
    LessonUpdateApiView, LessonDestroyApiView, PaymentsListAPIView, PaymentsCreateApiView, PaymentsUpdateAPIView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')


urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateApiView.as_view(), name='lesson_create'),
    path('lesson/retrieve/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson_retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateApiView.as_view(), name='lesson_update'),
    path('lesson/destroy/<int:pk>/', LessonDestroyApiView.as_view(), name='lesson_destroy'),
    path('payments/', PaymentsListAPIView.as_view(), name='payments_list'),
    path('payments/create/', PaymentsCreateApiView.as_view(), name='payments_create'),
    path('payments/update/<int:pk>/', PaymentsUpdateAPIView.as_view(), name='payments_update')
              ] + router.urls
