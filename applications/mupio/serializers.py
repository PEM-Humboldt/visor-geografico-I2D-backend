
from rest_framework import serializers

from .models import MpioRegisters,MpioSpecies

class mpioRegistersSerializer(serializers.ModelSerializer):
    class Meta:
        model= MpioRegisters
        fields =(
            'tipo',
            'count'
        )

class mpioSpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model= MpioSpecies
        fields =(
            'tipo',
            'count'
        )
