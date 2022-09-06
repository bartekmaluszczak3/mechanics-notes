from rest_framework import serializers
from .models import Car
from user_auth.models import User

class CarSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    class Meta:
        model = Car
        fields = ['brand', 'model', 'year', 'user_id']

    def create(self, validated_data):
        car = Car.objects.create(**validated_data)
        return car.as_json()
