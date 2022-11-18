# Generated by Django 4.0.8 on 2022-11-17 21:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='last_prediction_till_start_match_duration',
            field=models.DurationField(default=datetime.timedelta(seconds=300), help_text='day hour:minute:second', verbose_name='duration of last prediction time until start match'),
        ),
    ]