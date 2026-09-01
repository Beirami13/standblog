from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("register", views.user_register, name="register"),
    path("edit", views.edit_profile, name="edit"),
    path("create", views.create_profile, name="create_profile"),
]