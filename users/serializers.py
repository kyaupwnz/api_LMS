from rest_framework import serializers

from education.models import Payments
from users.models import User


class PaymentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentUserSerializer(many=True, source='payment_set', required=False)

    class Meta:
        model = User
        exclude = ['password']
