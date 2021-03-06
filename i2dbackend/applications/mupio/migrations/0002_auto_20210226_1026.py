# Generated by Django 3.1.7 on 2021-02-26 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mupio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mpio_tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveBigIntegerField(auto_created=True, serialize=False, verbose_name='cantidad')),
                ('mpio_ccnct', models.CharField(max_length=20, verbose_name='cod_mupio')),
                ('mpio_cnmbr', models.CharField(max_length=20, verbose_name='nomb_mupio')),
                ('types', models.CharField(max_length=20, verbose_name='tipo')),
            ],
        ),
        migrations.DeleteModel(
            name='Mupio_tipo',
        ),
    ]
