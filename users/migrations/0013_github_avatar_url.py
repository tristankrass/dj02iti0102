# Generated by Django 2.1.2 on 2018-12-13 08:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20181213_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='github',
            name='avatar_url',
            field=models.TextField(blank=True, validators=[django.core.validators.URLValidator], verbose_name='Avatar of the github user'),
        ),
    ]