from datetime import datetime

from django.core.management import BaseCommand

from education.models import Course, Lesson, Payments
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = []
        for user in User.objects.all():
            for i in range(10):
                payment_list.append(
                    Payments(
                        user=user,
                        payment_date=datetime.now(),
                        course=Course.objects.all().order_by('?').first(),
                        payment_sum=1000,
                        payment_type=Payments.CASHLESS
                    )
                )

        Payments.objects.bulk_create(payment_list)
