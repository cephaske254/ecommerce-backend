from django.urls import path
from . import views

urlpatterns = [
    path("order/", views.OrderAPIView.as_view()),
    path("order/<pk>/", views.OrderDetailAPIView.as_view()),
]
