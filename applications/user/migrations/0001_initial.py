# Generated by Django 3.1.7 on 2021-07-21 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id_solicitud', models.AutoField(primary_key=True, serialize=False)),
                ('entidad', models.CharField(blank=True, max_length=40, null=True)),
                ('nombre', models.CharField(blank=True, max_length=40, null=True)),
                ('email', models.CharField(blank=True, max_length=60, null=True)),
                ('observacion', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'solicitud',
                'managed': False,
            },
        ),
    ]
