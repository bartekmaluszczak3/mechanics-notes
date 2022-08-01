import datetime
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Note
from cars.models import Car
from .serializers import NoteSerializer


class PostNotesAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Note.objects.all()

    def post(self, request, id):
        car = Car.objects.filter(id=id).first()
        if car.id != request.user.id:
            return JsonResponse("You dont have access to this car", status=status.HTTP_403_FORBIDDEN)

        request.data['car_id'] = id
        if not 'date' in request.data:
            request.data['date'] = datetime.date.today()
        serializer = NoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        note = serializer.save()
        return JsonResponse(note, status=status.HTTP_200_OK)
