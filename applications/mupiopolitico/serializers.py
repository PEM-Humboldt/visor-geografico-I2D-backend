
from rest_framework import serializers

from .models import MpioPolitico

class mpioPoliticoSerializer(serializers.ModelSerializer):
    class Meta:
        model= MpioPolitico
        fields =(
            'gid',
            'nombre',
            'dpto_nombre',      
            'coord_central'     
        )

