from django.shortcuts import render

from rest_framework.generics import ListAPIView
from django.db.models import Q
from .models import MpioPolitico
from .serializers import mpioPoliticoSerializer

# Create your views here.

class mupioSearch(ListAPIView):
    serializer_class=mpioPoliticoSerializer

    def get_queryset(self):
        kword = self.kwargs['kword']
        queryParams = kword.split(",")

        numberParams = len(queryParams)
        q1 = queryParams[0]

        qmupios= MpioPolitico.objects.filter(mpio_cnmbr__istartswith=q1)[:5]
        
        if qmupios:
            if numberParams == 1:
                context = qmupios
            else:   
                q2 = queryParams[1] 
                context = MpioPolitico.objects.filter(Q(mpio_cnmbr__istartswith=q1) & Q(dpto_cnmbr__istartswith=q2))[:5]         
        else:
            if numberParams == 1:
                context = MpioPolitico.objects.filter(dpto_cnmbr__istartswith=q1)[:5]
            else:   
                q2 = queryParams[1]
                context = MpioPolitico.objects.filter(Q(dpto_cnmbr__istartswith=q1) & Q(mpio_cnmbr__istartswith=q2))[:5]
        return context
