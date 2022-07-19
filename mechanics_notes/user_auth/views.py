from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import generics, status

from .serializers import UserAuthSerializer
from .token import create_jwt


class RegisterView(generics.GenericAPIView):
    serializer_class = UserAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse({"message": "User was created"}, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt(user)
            return JsonResponse({"tokens": tokens}, status=status.HTTP_200_OK)
        return JsonResponse({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

