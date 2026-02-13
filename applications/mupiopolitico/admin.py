from django.contrib import admin
from django import forms
from django.contrib.gis.db import models as geomodels

from .models import MpioPolitico


@admin.register(MpioPolitico)
class MpioPoliticoAdmin(admin.ModelAdmin):
    # Render GeometryField as plain text area to ease manual paste/edit
    formfield_overrides = {
        geomodels.GeometryField: {
            'widget': forms.Textarea(attrs={
                'rows': 6,
                'cols': 100,
                'placeholder': 'Paste WKT/EWKT/GeoJSON geometry here'
            })
        }
    }
    list_display = ("gid", "codigo", "nombre", "dpto_nombre")
    search_fields = ("codigo", "nombre", "dpto_nombre")
