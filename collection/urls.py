from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("artwork/<int:artwork_id>", views.artwork, name="artwork"),
    path("search/", views.search, name="search"),
    path("accounts/profile/", views.index, name="profile"),  
    path("accounts/register/", views.register, name="register")
]
