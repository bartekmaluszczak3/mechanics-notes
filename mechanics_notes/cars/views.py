from django.http import JsonResponse
from rest_framework import generics, mixins, status
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request

from .permission import AuthorOrReadOnly
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
        return JsonResponse(car, status=status.HTTP_200_OK)


class GetSingleCarAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [AuthorOrReadOnly]

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GetAllCarsAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Car.objects.all()
    serializer_class = CarSerializer


    def get_queryset(self):
        user = self.request.user or None
        if user:
            return Car.objects.filter(user__email=user)
        return self.queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
