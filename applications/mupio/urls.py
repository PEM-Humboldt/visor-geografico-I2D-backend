from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/mpio/charts/<kid>', views.mpioQuery.as_view()),
    path('api/mpio/dangerCharts/<kid>', views.mpioDanger.as_view())
]
