from django.db import models
# from django.contrib.gis.db import models
# from django.contrib.postgres.indexes import GinIndex
# Create your models here.

class Solicitud(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    # fecha = models.DateField(blank=True, null=True) default calc on postgres
    entidad = models.CharField(max_length=40, blank=True, null=True)
    nombre = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    observacion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'solicitud'