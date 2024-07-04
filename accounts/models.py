from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username