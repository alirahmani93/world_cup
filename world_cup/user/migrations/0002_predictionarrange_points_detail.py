# Generated by Django 4.0.8 on 2022-11-17 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionarrange',
            name='points_detail',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='points detail'),
        ),
    ]