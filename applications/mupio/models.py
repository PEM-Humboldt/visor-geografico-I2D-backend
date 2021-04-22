from django.db import models

# Create your models here.

class MpioTipo(models.Model):
    mpio_ccnct = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    count = models.BigIntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    mpio_cnmbr = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mpio_tipo'
