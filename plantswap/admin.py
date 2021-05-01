from django.contrib import admin

from .models import Plant, Transaction, Reminder, Message, Match


class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'owner', 'added')
    search_fields = ('name', 'status', 'owner', 'added')
    readonly_fields = ('id', 'added')


admin.site.register(Plant, PlantAdmin)


class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'plant', 'previous_care_day',
                    'next_care_day', 'cycle', 'creator')
    search_fields = ('name', 'plant')
    readonly_fields = ('id', 'previous_care_day', 'next_care_day', 'creator')


admin.site.register(Reminder, ReminderAdmin)

admin.site.register(Match)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'finished')
    search_fields = ('plant', 'from_user', 'to_user')
    readonly_fields = ('id', 'message')


admin.site.register(Transaction, TransactionAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'from_user', 'to_user', 'content', 'date')
    search_fields = ('from_user', 'to_user', 'date')
    readonly_fields = ('id', 'content', 'date')


admin.site.register(Message, MessageAdmin)
