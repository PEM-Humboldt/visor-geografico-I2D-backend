from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/gbif/gbifinfo', views.GbifInfo.as_view()),
    path('api/gbif/descargar-zip/', views.descargar_zip, name='descargar_zip'),
]
