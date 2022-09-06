from django.urls import path
from .views import PostCarAPIView, GetSingleCarAPIView, GetAllCarsAPIView
urlpatterns = [
    path('', PostCarAPIView.as_view()),
    path('<int:pk>', GetSingleCarAPIView.as_view(), name="get_single"),
    path('all/', GetAllCarsAPIView.as_view(), name="all_cars")

]
