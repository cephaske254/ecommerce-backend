from django.urls import path
from . import views


urlpatterns = [
    path('verify_email/<slug:uidb64>/<slug:token>/', views.verify_email, name="verify_email")
]