# Generated by Django 4.0.8 on 2022-11-18 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_predictionarrange_points_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='mobile_number',
            field=models.CharField(max_length=31, unique=True, verbose_name='Mobile number'),
        ),
    ]
