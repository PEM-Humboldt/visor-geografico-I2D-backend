from django.shortcuts import render

from rest_framework.generics import ListAPIView

from .models import MpioTipo
from .serializers import mpioChartSerializer

class mupioChart(ListAPIView):
    serializer_class=mpioChartSerializer

    def get_queryset(self):
        kid = self.kwargs['kid']
        return MpioTipo.objects.filter(mpio_ccnct=kid).exclude(tipo__isnull=True)


#     raw_sql = MpioTipo.objects.raw("SELECT 1 as id,array_to_json(array_agg(row_to_json(mpio))) FROM (SELECT tipo as type,count as total FROM mpio_tipo WHERE mpio_ccnct=  %s AND tipo IS NOT NULL)as mpio", [lname])
#     for i in raw_sql:
#         print(i.array_to_json)
