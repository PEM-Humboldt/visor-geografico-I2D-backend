from django.shortcuts import render

from rest_framework.generics import ListAPIView
from .models import MpioQueries, MpioAmenazas
from .serializers import mpioQueriesSerializer,mpioDangerSerializer

class mpioQuery(ListAPIView):
    serializer_class=mpioQueriesSerializer

    def get_queryset(self):
        kid = self.kwargs['kid']
        return MpioQueries.objects.filter(codigo=kid).exclude(tipo__isnull=True).distinct('tipo')


class mpioDanger(ListAPIView):
    serializer_class=mpioDangerSerializer

    def get_queryset(self):
        kid = self.kwargs['kid']
        return MpioAmenazas.objects.filter(codigo=kid).exclude(tipo__isnull=True)
