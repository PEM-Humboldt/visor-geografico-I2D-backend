from django.db import models
# from django.contrib.gis.db import models

# Create your models here.

class MpioPolitico(models.Model):
    gid = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=5, blank=True, null=True)
    dpto_nombre = models.CharField(max_length=254, blank=True, null=True)
    nombre = models.CharField(max_length=254, blank=True, null=True)
    nombre_unaccented = models.CharField(max_length=254, blank=True, null=True)
    area_ha = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    coord_central = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mpio_politico'