# Generated by Django 4.0 on 2022-09-04 07:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPosting',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='timeline')),
                ('caption', models.TextField()),
                ('uploaded_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
