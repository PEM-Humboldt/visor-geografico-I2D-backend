from django.db import models
# from django.contrib.postgres.indexes import GinIndex
# Create your models here.

class MpioRegisters(models.Model):
    codigo = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    count = models.BigIntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nombre = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mpio_registers'

class MpioSpecies(models.Model):
    codigo = models.CharField(max_length=5, blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    count = models.BigIntegerField(blank=True, null=True)
    geom = models.TextField(blank=True, null=True)  # This field type is a guess.
    nombre = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mpio_species'


# from django.db import models

# # Create your models here.

# class Mupio_tipo(models.Model):
#     mpio_ccnct= models.CharField('cod_mupio',max_length=20,primary_key = True)
#     tipo= models.CharField('tipo',max_length=20)
#     count= models.PositiveBigIntegerField(auto_created = True, 
#     serialize = False, 
#     verbose_name ='cantidad')
#     mpio_cnmbr= models.CharField('nomb_mupio',max_length=20)

#     # class Meta:
#     #     verbose_name = "Tipo por municipio"
#     #     verbose_name_plural = "Tipos por municipio"
#     #     ordering =['-mpio_cnmbr']
        
#     def __str__(self):
#         return self.mpio_ccnct+'-'+self.tipo