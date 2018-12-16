# Generated by Django 2.1.2 on 2018-11-12 09:55

from django.db import migrations, models
import hashid_field.field


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='body')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created timestamp')),
            ],
            options={
                'ordering': ('-created_timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', hashid_field.field.HashidAutoField(alphabet='abcdefghijklmnopqrstuvwxyz0123456789', min_length=7, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('body', models.TextField(blank=True, verbose_name='body')),
                ('created_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='created timestamp')),
            ],
            options={
                'ordering': ('-created_timestamp',),
            },
        ),
    ]
