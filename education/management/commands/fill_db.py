from django.core.management import BaseCommand

from education.models import Course, Lesson, Payments
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = [
            {'email': 'test@test.ru', 'city': 'Moscow', },
            {'email': 'test2@test.ru', 'city': 'Tomsk', }
        ]
        courses = [
            {'title': 'Курс номер один', 'description': 'Очень важный курс'},
            {'title': 'Курс номер два', 'description': 'Не менее важный курс'}
        ]
        lessons = [
            {'title': 'Первый урок', 'video_url': 'https://youtube.com/1', 'description': 'Первый важный урок'},
            {'title': 'Второй урок', 'video_url': 'https://youtube.com/2', 'description': 'Второй важный урок'}
        ]
        payments = [
            {'user': '1', 'course': '1', 'payment_sum': '15000'},
            {'user': '1', 'lesson': '1', 'payment_sum': '20000'},
            {'user': '2', 'course': '2', 'payment_sum': '10000', 'payment_type': 'cashless'}
        ]
        users_list = []
        courses_list = []
        lessons_list = []
        payments_list = []

        for item in users:
            users_list.append(User(**item))

        for item in courses:
            courses_list.append(Course(**item))

        for item in lessons:
            lessons_list.append(Lesson(**item))

        for item in payments:
            payments_list.append(Payments(**item))

        User.objects.all().delete()
        User.objects.bulk_create(users_list)

        Course.objects.all().delete()
        Course.objects.bulk_create(courses_list)

        Lesson.objects.all().delete()
        Lesson.objects.bulk_create(lessons_list)

        Payments.objects.all().delete()
        Payments.objects.bulk_create(payments_list)
