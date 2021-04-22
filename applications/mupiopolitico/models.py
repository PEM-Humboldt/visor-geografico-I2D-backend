from django.db import models
# from django.contrib.gis.db import models

# Create your models here.

class MpioPolitico(models.Model):
    gid = models.IntegerField(primary_key=True)
    dpto_ccdgo = models.CharField(max_length=2, blank=True, null=True)
    mpio_ccdgo = models.CharField(max_length=3, blank=True, null=True)
    mpio_cnmbr = models.CharField(max_length=60, blank=True, null=True)
    mpio_crslc = models.CharField(max_length=60, blank=True, null=True)
    mpio_narea = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    mpio_ccnct = models.CharField(max_length=5, blank=True, null=True)
    mpio_nano = models.BigIntegerField(blank=True, null=True)
    dpto_cnmbr = models.CharField(max_length=250, blank=True, null=True)
    shape_area = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    shape_len = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    orig_fid = models.BigIntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    center_coord = models.TextField(blank=True, null=True)
    class Meta:
        # indexes = [
        #     GinIndex(fields=['mpio_cnmbr'], name='search_mpio_cnmbr_idx')
        # ]
        managed = False
        db_table = 'mpio_politico'