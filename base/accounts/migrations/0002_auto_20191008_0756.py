# Generated by Django 2.2.4 on 2019-10-08 02:26

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='date_of_joining',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='myuser',
            name='dirtybit',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
