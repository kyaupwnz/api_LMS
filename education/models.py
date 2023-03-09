from django.conf import settings
from django.db import models

from users.models import NULLABLE


# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    preview = models.ImageField(upload_to='education/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='Описание')


    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', **NULLABLE)
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview = models.ImageField(upload_to='education/', verbose_name='Превью', **NULLABLE)
    video_url = models.URLField(verbose_name='Cсылка на видео')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Payments(models.Model):
    CASH = 'cash'
    CASHLESS = 'cashless'
    PAYMENT_TYPE = [
        (CASH, 'cash'),
        (CASHLESS, 'cashless')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(auto_now_add=True, verbose_name='Дата платежа')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Оплаченный урок', **NULLABLE)
    payment_sum = models.IntegerField(verbose_name='Сумма оплаты')
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=20, default=CASH, verbose_name='Способ оплаты')


    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    status = models.BooleanField(default=True)
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE, verbose_name='Платеж')