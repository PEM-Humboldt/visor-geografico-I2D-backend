
from rest_framework import serializers

from .models import MpioTipo

class mpioChartSerializer(serializers.ModelSerializer):
    class Meta:
        model= MpioTipo
        fields =(
            'tipo',
            'count'
        )
