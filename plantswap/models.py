from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(null=True)
    photo = models.ImageField(upload_to='plants', null=True)
    amount = models.SmallIntegerField(default=0)

    # zdjęcie (image) ** opcjonalne
    # opis (description) ** opcjonalne
    # ziemia (ground) ** opcjonalne
    # podlewanie (water) ** opcjonalne
    # właściciel (owner, FK User)

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

    # tworca(creator, FK User)

    def __str__(self):
        return self.name
