from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/requestcreate/', views.userSolicitudCreateAPIView.as_view())
]
