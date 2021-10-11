
from rest_framework import serializers

from .models import DptoQueries,DptoAmenazas

class dptoQueriesSerializer(serializers.ModelSerializer):
    class Meta:
        model= DptoQueries
        fields =(
            'tipo',
            'registers',
            'species',
            'exoticas',
            'endemicas'
        )

class dptoDangerSerializer(serializers.ModelSerializer):
    class Meta:
        model= DptoAmenazas
        fields =(
            'codigo',
            'tipo',
            'amenazadas',
            'nombre'
        )
