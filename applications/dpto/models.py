from django.db import models
# from django.contrib.gis.db import models
# from django.contrib.postgres.indexes import GinIndex
# Create your models here.

class DptoQueries(models.Model):
    codigo = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    registers = models.BigIntegerField(blank=True, null=True)    
    species = models.BigIntegerField(blank=True, null=True) 
    exoticas = models.BigIntegerField(blank=True, null=True)
    endemicas = models.BigIntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.    
    # geom = models.GeometryField(blank=True, null=True)      
    nombre = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dpto_queries'


class DptoAmenazas(models.Model):
    codigo = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    amenazadas = models.BigIntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)
    # geom = models.GeometryField(blank=True, null=True)
    nombre = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dpto_amenazas'



# from django.db import models

# # Create your models here.

# class Mupio_tipo(models.Model):
#     dpto_ccnct= models.CharField('cod_mupio',max_length=20,primary_key = True)
#     tipo= models.CharField('tipo',max_length=20)
#     count= models.PositiveBigIntegerField(auto_created = True, 
#     serialize = False, 
#     verbose_name ='cantidad')
#     dpto_cnmbr= models.CharField('nomb_mupio',max_length=20)

#     # class Meta:
#     #     verbose_name = "Tipo por municipio"
#     #     verbose_name_plural = "Tipos por municipio"
#     #     ordering =['-dpto_cnmbr']
        
#     def __str__(self):
#         return self.dpto_ccnct+'-'+self.tipo