from django.shortcuts import render
from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import MpioPolitico
from .serializers import mpioPoliticoSerializer
from unidecode import unidecode

class mupioSearch(ListAPIView):
    serializer_class = mpioPoliticoSerializer

    def get_queryset(self):
        kword = self.kwargs['kword']
        queryParams = unidecode(kword).split(",")
        numberParams = len(queryParams)
        q1 = unidecode(queryParams[0])

        qmupios = MpioPolitico.objects.filter(
            Q(nombre__icontains=q1) | Q(nombre_unaccented__icontains=q1)
        )[:5]

        if qmupios and numberParams > 1:
            q2 = unidecode(queryParams[1])
            qmupios = qmupios.filter(
                Q(dpto_nombre__icontains=q2) | Q(dpto_nombre_unaccented__icontains=q2)
            )[:5]

        return qmupios
