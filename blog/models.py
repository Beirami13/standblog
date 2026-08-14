from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/article")
    updated = models.DateTimeField(auto_now=True)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.title} - {self.content[:30]} "

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})