from django.urls import path

from .views import PostNotesAPIView
urlpatterns = [
    path('<int:id>', PostNotesAPIView.as_view(), name="notes")
]