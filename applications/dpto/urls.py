from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/dpto/charts/<kid>', views.dptoQuery.as_view()),
    path('api/dpto/dangerCharts/<kid>', views.dptoDanger.as_view())
]
