from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Plant(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to='plants', null=True)
    amount = models.SmallIntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)

    # owner = models.ForeignKey(User)

    # ziemia (ground) ** opcjonalne
    # podlewanie (water) ** opcjonalne

    def __str__(self):
        return self.name


class Transaction(models.Model):
    STATUS_CHOICE = (
        (1, 'Sprzedam'),
        (2, 'Wymienię'),
        (3, 'Oddam')
    )

    name = models.CharField(max_length=128)
    description = models.TextField()
    plant = models.ManyToManyField(Plant)
    status = models.IntegerField(choices=STATUS_CHOICE)
    created_at = models.DateField(auto_now_add=True)

    # tworca(creator, FK User)

    def __str__(self):
        return self.name
