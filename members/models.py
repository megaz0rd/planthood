import requests
from django.db import models
from django.contrib.auth import get_user_model

from planthood.settings import GOOGLE_MAPS_API_KEY

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    street = models.CharField(max_length=64)
    building_number = models.CharField(max_length=8)
    city = models.CharField(max_length=32, default='Warszawa')
    latitude = models.DecimalField(max_digits=9, decimal_places=6,
                                   blank=True, default=0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6,
                                    blank=True, default=0)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        if GOOGLE_MAPS_API_KEY:
            address = " ".join(
                [self.street, str(self.building_number), self.city])
            api_response = requests.get(
                'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(
                    address, GOOGLE_MAPS_API_KEY))
            api_response_dict = api_response.json()
            if api_response_dict['status'] == 'OK':
                self.latitude = \
                    api_response_dict['results'][0]['geometry']['location'][
                        'lat']
                self.longitude = \
                    api_response_dict['results'][0]['geometry']['location'][
                        'lng']

            super(UserProfile, self).save(*args, **kwargs)
        else:
            super(UserProfile, self).save(*args, **kwargs)
