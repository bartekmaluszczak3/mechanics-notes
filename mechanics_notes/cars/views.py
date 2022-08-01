from django.http import JsonResponse
from rest_framework import generics, mixins, status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request

from mechanics_notes.permission import AuthorOrReadOnly
from .models import Car
from .serializers import CarSerializer


class PostCarAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Car.objects.all()

    def post(self, request):
        user = self.request.user.id
        request.data['user_id'] = user
        serializer = CarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.save()
        return JsonResponse(car.as_json(), status=status.HTTP_200_OK)


class GetSingleCarAPIView(generics.GenericAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AuthorOrReadOnly]

    def get(self, request, pk):
        car = Car.objects.filter(id=pk).first()
        return JsonResponse(car.as_json(), status=status.HTTP_200_OK)


class GetAllCarsAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    def get(self, request):
        user = request.user
        query_cars = Car.objects.filter(user__email=user)
        cars = [car.as_json() for car in query_cars]
        return JsonResponse(cars, status=status.HTTP_200_OK, safe=False)