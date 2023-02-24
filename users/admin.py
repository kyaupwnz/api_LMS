from django.contrib import admin

from education.models import Payments
from users.models import User

# Register your models here.
admin.site.register(User)

admin.site.register(Payments)
