from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('mupio/', views.mupioChart.as_view()),
    path('api/mpio/chartdata/<kid>', views.mupioChart.as_view()),
]
