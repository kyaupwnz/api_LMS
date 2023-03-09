from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from rest_framework import status
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY

from education.models import Course
from users.models import User


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User(email='manager@test.ru', is_staff=True, is_active=True)
        self.user.set_password('manager')
        self.user.save()
        permission = Permission.objects.get(name='Can add Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can delete Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can view Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can change Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can add Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can delete Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can view Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can change Урок')
        self.user.user_permissions.add(permission)
        self.user.save()
        response = self.client.post("/users/api/token/", {"email": "manager@test.ru", "password": "manager"})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.test_data = {
            "title": "Первый курс",
            "description": "Интересный курс",
            "lesson": [
                {
                    "title": "первый урок",
                    "description": "описание урока",
                    "video_url": "https://youtube.com"
                }
            ]
        }
        self.test_response_data = {
            "id": 1,
            "title": "Первый курс",
            "description": "Интересный курс",
            "lesson": [
                {
                    "id": 1,
                    "title": "первый урок",
                    "description": "описание урока",
                    "video_url": "https://youtube.com"
                }
            ],
            "lesson_count": 1,
            "subs_status": False
        }

    def test_course_create(self):
        print(self.test_data)
        response = self.client.post("/education/course/", self.test_data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), self.test_response_data)


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User(email='manager@test.ru', is_staff=True, is_active=True)
        self.user.set_password('manager')
        self.user.save()
        permission = Permission.objects.get(name='Can add Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can delete Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can view Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can change Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can add Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can delete Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can view Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can change Урок')
        self.user.user_permissions.add(permission)
        self.user.save()
        response = self.client.post("/users/api/token/", {'email': 'manager@test.ru', 'password': 'manager'})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.test_data = {
                "title": "Первый урок седьмого курса",
                "description": "Описание первого урока седьмого курса",
                "video_url": "https://youtube.com"
            }
        self.test_response_data = {
            "id": 1,
            "title": "Первый урок седьмого курса",
            "description": "Описание первого урока седьмого курса",
            "video_url": "https://youtube.com"
        }

    def test_lesson_create(self):
        response = self.client.post("/education/lesson/create/", self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), self.test_response_data)

    def test_lesson_list(self):
        self.test_lesson_create()
        response = self.client.get('/education/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [self.test_response_data])

    def test_lesson_update(self):
        self.test_lesson_create()
        response = self.client.patch("/education/lesson/update/1/", {
            "title": "test",
            "video_url": "https://youtube.com/test"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_data = {"id": 1, "title": "test", "description": "Описание первого урока седьмого курса", "video_url": "https://youtube.com/test"}
        self.assertEqual(response.json(), updated_data)

    def test_lesson_detail(self):
        self.test_lesson_create()
        response = self.client.get('/education/lesson/retrieve/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), self.test_response_data)

    def test_lesson_delete(self):
        self.test_lesson_create()
        response = self.client.delete('/education/lesson/destroy/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PaymentsTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User(email='test@test.ru', is_active=True)
        self.user.set_password('testuser')
        self.user.save()
        permission = Permission.objects.get(name='Can add Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can delete Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can view Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can change Курс')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can add Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can delete Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can view Урок')
        self.user.user_permissions.add(permission)
        permission = Permission.objects.get(name='Can change Урок')
        self.user.user_permissions.add(permission)
        self.user.save()
        response = self.client.post("/users/api/token/", {'email': 'test@test.ru', 'password': 'testuser'})
        self.access_token = response.json().get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        course_data =   {
                "title": "Первый курс",
                "description": "Интересный курс",
                "lesson": [
                    {
                        "title": "первый урок",
                        "description": "описание урока",
                        "video_url": "https://youtube.com"
                    }
                ]
            }
        self.course = Course.objects.get_or_create(course_data)

        self.test_data = {
            "payment_sum": 15000,
            "course": 1,
        }
        self.test_response_data = {
            "id": 1,
            "user": "test@test.ru",
            "subs_status": True,
            "payment_date": "2023-03-09",
            "payment_sum": 15000,
            "payment_type": "cash",
            "course": 1,
            "lesson": None
        }

    def test_payments_create(self):
        response = self.client.post("/education/payments/create/", self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), self.test_response_data)

    def test_payments_update(self):
        self.test_payments_create()
        response = self.client.patch('/education/payments/update/1/')
        print(response.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_data = {
            "id": 1,
            "user": "test@test.ru",
            "subs_status": False,
            "payment_date": "2023-03-09",
            "payment_sum": 15000,
            "payment_type": "cash",
            "course": 1,
            "lesson": None
        }
        self.assertEqual(response.json(), updated_data)
