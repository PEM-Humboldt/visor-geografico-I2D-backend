from django.contrib.gis.db import models
# from django.contrib.postgres.indexes import GinIndex
# Create your models here.

class MpioQueries(models.Model):
    codigo = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    registers = models.BigIntegerField(blank=True, null=True)
    species = models.BigIntegerField(blank=True, null=True)
    exoticas = models.BigIntegerField(blank=True, null=True)
    endemicas = models.BigIntegerField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    nombre = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mpio_queries'


class MpioAmenazas(models.Model):
    codigo = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    amenazadas = models.BigIntegerField(blank=True, null=True)
    geom = models.GeometryField(blank=True, null=True)
    nombre = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mpio_amenazas'
