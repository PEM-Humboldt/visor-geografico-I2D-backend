
from rest_framework import serializers

from .models import gbifInfo

class gbifInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model= gbifInfo
        fields =(
            '__all__'
        )
