from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'street', 'building_number', 'latitude',
                    'longitude')
    search_fields = ('user', 'street', 'building_number', 'latitude',
                     'longitude')
    readonly_fields = ('id',)


admin.site.register(UserProfile, UserProfileAdmin)
