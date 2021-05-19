from datetime import timedelta

from django.conf import settings
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, GEOSGeometry
from django.urls import reverse_lazy

from plantswap.constant import CARE_TYPE, STATUS_CHOICE
from plantswap.validators import validate_date


class Plant(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    photo = models.ImageField(upload_to='plants/', null=True, blank=True)
    added = models.DateField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('plantswap:plant-detail', args=[str(self.pk)])

    def get_add_to_transaction_url(self):
        return reverse_lazy('plantswap:add-to-transaction',
                            args=[str(self.pk)])

    def save(self, *args, **kwargs):
        self.location = GEOSGeometry(
            f'SRID=4326;POINT({self.owner.userprofile.latitude} '
            f'{self.owner.userprofile.longitude})')
        super(Plant, self).save(*args, **kwargs)


class Message(models.Model):
    plant = models.ForeignKey(Plant,
                              related_name='comments',
                              on_delete=models.SET_NULL, null=True)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET_NULL,
                                  related_name='sender', null=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                related_name='recipient', null=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.content


class Transaction(models.Model):
    plant = models.ForeignKey(Plant,
                              related_name='match',
                              on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                related_name='taker')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  related_name='owner')
    is_finished = models.BooleanField(default=False)
    message = models.ManyToManyField(Message)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return 'Transaction between: ' + self.to_user.username + ' and ' + \
               self.from_user.username

    def get_absolute_url(self):
        return reverse_lazy('plantswap:transaction-detail',
                            args=[str(self.pk)])


class Reminder(models.Model):
    name = models.CharField(max_length=9, choices=CARE_TYPE, default='WATER')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    previous_care_day = models.DateField(validators=[validate_date])
    cycle = models.SmallIntegerField(default=7)
    next_care_day = models.DateField()  # field not visible for user
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['next_care_day']

    def save(self, *args, **kwargs):
        self.next_care_day = self.previous_care_day + timedelta(
            days=self.cycle)
        super(Reminder, self).save(*args, **kwargs)

    def __str__(self):
        return self.plant.name + ' ' + self.name
