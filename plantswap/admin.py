from django.contrib import admin

from .models import Plant, Transaction, Reminder

admin.site.register(Plant),
admin.site.register(Transaction)
admin.site.register(Reminder)
