from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .models import gbifInfo
from .serializers import gbifInfoSerializer

class GbifInfo(ListAPIView):
    serializer_class=gbifInfoSerializer

    def get_queryset(self):
        return gbifInfo.objects.all() 

