from rest_framework import serializers

from plantswap.models import Plant, Transaction


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = [
            'id',
            'name',
            'description',
            'photo',
            'amount',
            'created_at',
        ]


class TransactionSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    plant = PlantSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'name',
            'description',
            'plant',
            'created_at',
            'status',
            'status_display'
        ]

    def get_status_display(self, obj):
        return obj.get_status_display()
