from django.db import models

# Create your models here.

class gbifInfo(models.Model):
    download_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'gbif_info'
