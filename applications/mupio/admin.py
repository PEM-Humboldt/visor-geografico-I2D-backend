from django.contrib import admin
from django import forms
from django.contrib.gis.db import models as geomodels
from .models import MpioQueries, MpioAmenazas


@admin.register(MpioQueries)
class MpioQueriesAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.GeometryField: {
            'widget': forms.Textarea(attrs={
                'rows': 6,
                'cols': 100,
                'placeholder': 'Paste WKT/EWKT/GeoJSON geometry here'
            })
        }
    }
    list_display = ("codigo", "tipo", "nombre")
    search_fields = ("codigo", "nombre", "tipo")


@admin.register(MpioAmenazas)
class MpioAmenazasAdmin(admin.ModelAdmin):
    formfield_overrides = {
        geomodels.GeometryField: {
            'widget': forms.Textarea(attrs={
                'rows': 6,
                'cols': 100,
                'placeholder': 'Paste WKT/EWKT/GeoJSON geometry here'
            })
        }
    }
    list_display = ("codigo", "tipo", "amenazadas", "nombre")
    search_fields = ("codigo", "nombre", "tipo")