# Generated migration to add color field to LayerGroup

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='layergroup',
            name='color',
            field=models.CharField(
                default='#e3e3e3',
                help_text='Hexadecimal color code for the layer group (e.g., #FF5733)',
                max_length=7,
                validators=[
                    django.core.validators.RegexValidator(
                        code='invalid_color',
                        message='Enter a valid hexadecimal color code (e.g., #FF5733 or #F57)',
                        regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
                    )
                ]
            ),
        ),
    ]
