
from rest_framework import serializers

from .models import MpioQueries,MpioAmenazas

class mpioQueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model= MpioQueries
        fields =(
            'tipo',
            'registers',
            'species',
            'exoticas',
            'endemicas'
        )

class mpioDangerSerializer(serializers.ModelSerializer):
    class Meta:
        model= MpioAmenazas
        fields =(
            'codigo',
            'tipo',
            'amenazadas',
            'nombre'
        )
