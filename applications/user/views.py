from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from .serializers import SolicitudSerializer

class userSolicitudCreateAPIView (CreateAPIView):
    serializer_class=SolicitudSerializer  
