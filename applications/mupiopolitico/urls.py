from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # path('mupio/', views.mupioChart.as_view()),
    path('api/mpio/search/<kword>', views.mupioSearch.as_view()),
]
