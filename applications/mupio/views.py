from django.shortcuts import render

from rest_framework.generics import ListAPIView
from .models import MpioRegisters,MpioSpecies
from .serializers import mpioRegistersSerializer,mpioSpeciesSerializer

class mupioRegister(ListAPIView):
    serializer_class=mpioRegistersSerializer

    def get_queryset(self):
        kid = self.kwargs['kid']
        return MpioRegisters.objects.filter(codigo=kid).exclude(tipo__isnull=True).distinct('tipo')

class mupioSpecie(ListAPIView):
    serializer_class=mpioSpeciesSerializer

    def get_queryset(self):
        kid = self.kwargs['kid']
        return MpioSpecies.objects.filter(codigo=kid).exclude(tipo__isnull=True).distinct('tipo')
