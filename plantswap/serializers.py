from rest_framework import serializers

from plantswap.models import Plant, Transaction


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
            'finished'
        ]
