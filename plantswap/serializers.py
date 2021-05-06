from django.contrib.auth.models import User, Group
from rest_framework import serializers

from plantswap.models import Plant, Reminder, Transaction


class PlantSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = [
            'id',
            'name',
            'description',
            'photo',
            'added',
            'status',
            'status_display',
            'owner'
        ]

    def get_status_display(self, obj):
        return obj.get_status_display()


class TransactionSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(many=False, read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'plant',
            'to_user',
            'from_user',
            'is_finished'
        ]


class ReminderSerializer(serializers.ModelSerializer):
    plant = PlantSerializer(many=False, read_only=True)

    class Meta:
        model = Reminder
        fields = [
            'name',
            'plant',
            'cycle',
            'previous_care_day',
            'next_care_day',
            'creator'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']
