from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/profile/", views.index, name="profile"),  # Nueva vista para el perfil
    path("accounts/register/", views.register, name="register")
]
