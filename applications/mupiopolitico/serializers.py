
from rest_framework import serializers

from .models import MpioPolitico

class mpioPoliticoSerializer(serializers.ModelSerializer):
    class Meta:
        model= MpioPolitico
        fields =(
            'gid',
            'mpio_cnmbr',
            'dpto_cnmbr',      
            'center_coord'      
        )

