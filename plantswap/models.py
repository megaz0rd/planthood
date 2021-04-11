from django.db import models
from django.contrib.auth import get_user_model

from plantswap.constant import CARE_TYPE, STATUS_CHOICE
from plantswap_api.utils import today

User = get_user_model()


class Plant(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to='plants', null=True)
    amount = models.SmallIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    # owner = models.ForeignKey(User)
    # typ (type) = models.ChoiceField
    # ziemia (ground) ** opcjonalne
    # podlewanie (water) ** opcjonalne

    def __str__(self):
        return self.name


class Transaction(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    plant = models.ManyToManyField(Plant)
    status = models.IntegerField(choices=STATUS_CHOICE)
    created_at = models.DateField(auto_now_add=True)

    # tworca(creator, FK User)

    def __str__(self):
        return self.name


class Reminder(models.Model):
    name = models.CharField(max_length=9, choices=CARE_TYPE, default='WATER')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    previous_care_day = models.DateField()
    cycle = models.SmallIntegerField(default=7)

    # field not visible for user
    next_care_day = models.DateField()

    def __str__(self):
        return self.plant.name + self.name

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     street = models.CharField(max_length=64)
#     building_number = models.CharField(max_length=8)
