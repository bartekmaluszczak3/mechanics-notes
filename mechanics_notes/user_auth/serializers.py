from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from rest_framework import serializers

from .models import User


class UserAuthSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, max_length=16)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError("User with this e-mail already exists")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user
