from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fathers_name = models.CharField(max_length=100)
    national_code = models.IntegerField()
    image = models.ImageField(upload_to='profiles/images')
