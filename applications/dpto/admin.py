from django.contrib import admin
from django import forms
from django.contrib.gis.db import models as geomodels
from .models import DptoQueries, DptoAmenazas

# Register your models here.

@admin.register(DptoQueries)
class DptoQueriesAdmin(admin.ModelAdmin):
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


@admin.register(DptoAmenazas)
class DptoAmenazasAdmin(admin.ModelAdmin):
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