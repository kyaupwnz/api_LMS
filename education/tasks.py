import hashlib

import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from education.models import Payments, PaymentLog


@shared_task
def course_update_notify(course_pk):
    payment = Payments.objects.filter(course=course_pk)
    for item in payment:
        send_mail(
            subject='Курс был обновлен',
            message='Курс был обновлен, проверьте изменения',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[item.user.email],
            fail_silently=False
        )
        print(f'Письмо отправлено {item.user.email}')


@shared_task
def status_check():
    data = PaymentLog.objects.filter(Status='NEW')
    if data.exists():
        for item in data:
            token = hashlib.sha256(f"{settings.TERMINAL_PASSWORD}{item.PaymentId}{settings.TERMINAL_KEY}".encode())
            token = token.hexdigest()

            request_data = {
                "TerminalKey": settings.TERMINAL_KEY,
                "PaymentId": item.PaymentId,
                "Token": token
            }
            response = requests.post('https://securepay.tinkoff.ru/v2/GetState', json=request_data)
            print(response.json())
            item.Status = response.json().get('Status')
            item.save()