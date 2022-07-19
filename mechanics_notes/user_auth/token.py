from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def create_jwt(user: User):
    tokens = RefreshToken.for_user(user)

    return {"access": str(tokens.access_token), "refresh": str(tokens)}
