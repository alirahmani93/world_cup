# Generated by Django 4.1.2 on 2022-10-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_correctpredictscore'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='by_pass_sms',
            field=models.BooleanField(default=False, verbose_name='by pass sms'),
        ),
        migrations.AddField(
            model_name='correctpredictscore',
            name='best_player_score',
            field=models.PositiveIntegerField(default=1, verbose_name='best player score'),
        ),
    ]
