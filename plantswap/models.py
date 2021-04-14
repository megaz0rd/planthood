from django.db import models
from django.urls import reverse_lazy

from plantswap.constant import CARE_TYPE, STATUS_CHOICE


class Plant(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to='plants', blank=True)
    created_at = models.DateField(auto_now_add=True)

    # owner = models.ForeignKey(User)
    # typ (type) = models.ChoiceField
    # ziemia (ground) ** opcjonalne
    # podlewanie (water) ** opcjonalne

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse_lazy('plantswap:plant-detail', args=[str(self.pk)])


class Transaction(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    plant = models.ManyToManyField(Plant)
    status = models.IntegerField(choices=STATUS_CHOICE)
    amount = models.SmallIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    # tworca(creator, FK User)

    def __str__(self):
        return self.name


class Reminder(models.Model):
    name = models.CharField(max_length=9, choices=CARE_TYPE, default='WATER')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    previous_care_day = models.DateField()
    cycle = models.SmallIntegerField(default=7)

    # # field not visible for user
    # next_care_day = models.DateField()

    def __str__(self):
        return self.plant.name + ' ' + self.name
