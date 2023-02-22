from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class CustomUserManager(UserManager):

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(unique=True, max_length=15, verbose_name='Номер телефона', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='Страна')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
