# Generated by Django 4.0 on 2022-09-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0002_userposting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='location',
            field=models.CharField(blank=True, default='None', max_length=100),
        ),
    ]
