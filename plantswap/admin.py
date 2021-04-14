from django.contrib import admin

from .models import Plant, Transaction

admin.site.register(Plant),
admin.site.register(Transaction)

