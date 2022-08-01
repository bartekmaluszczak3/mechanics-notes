from rest_framework import serializers
from .models import Note
from cars.models import Car


class NoteSerializer(serializers.ModelSerializer):
    car_id = serializers.IntegerField()

    class Meta:
        model = Note
        fields = ['description', 'mileage', 'repair', 'next_repair', 'car_id', 'date']

    def create(self, validated_data):
        note = Note.objects.create(**validated_data)
        return note.as_json()
