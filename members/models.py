from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    street = models.CharField(max_length=64)
    building_number = models.CharField(max_length=8)

    def __str__(self):
        return self.user.email
