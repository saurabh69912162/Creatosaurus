# Generated by Django 2.2.4 on 2019-10-19 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0040_temp_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temp_data',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]