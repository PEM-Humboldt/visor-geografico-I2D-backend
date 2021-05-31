from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/mpio/registers/<kid>', views.mupioRegister.as_view()),
    path('api/mpio/species/<kid>', views.mupioSpecie.as_view()),
]
