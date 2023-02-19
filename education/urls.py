from django.urls import path
from rest_framework.routers import DefaultRouter

from education.views import CourseViewSet, LessonListView, LessonCreateApiView, LessonRetrieveUpdateDestroyApiView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')



urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateApiView.as_view(), name='lesson_create'),
    path('lesson/retrieveupdatedestroy/', LessonRetrieveUpdateDestroyApiView.as_view(), name='lesson_retrieveupdatedestroy')
              ] + router.urls
