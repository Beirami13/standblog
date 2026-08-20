from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('details/<slug:slug>', views.post_detail, name='post_detail'),
    path('posts', views.posts_list, name='posts_list'),
    path('category/<int:pk>', views.categories_detail, name='category'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact_us, name='contact_us'),
    path('contact-messages/',views.contact_messages,name='contact_messages'),
]