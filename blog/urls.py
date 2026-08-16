from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('details/<slug:slug>', views.post_detail, name='post_detail'),
    path('posts', views.posts_list, name='posts_list'),
]