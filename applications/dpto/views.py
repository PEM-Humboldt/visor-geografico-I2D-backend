from django.shortcuts import render

from rest_framework.generics import ListAPIView
from .models import DptoQueries, DptoAmenazas
from .serializers import dptoQueriesSerializer,dptoDangerSerializer

class dptoQuery(ListAPIView):
    serializer_class=dptoQueriesSerializer

    def get_queryset(self):
        kid = self.kwargs['kid']
        return DptoQueries.objects.filter(codigo=kid).exclude(tipo__isnull=True).distinct('tipo')


class dptoDanger(ListAPIView):
    serializer_class=dptoDangerSerializer

    def get_queryset(self):
        kid = self.kwargs['kid']
        return DptoAmenazas.objects.filter(codigo=kid).exclude(tipo__isnull=True)
