# Generated by Django 4.1.2 on 2022-11-10 15:41

import common.models
import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('app_name', models.CharField(default=common.models.Configuration.get_app_name, max_length=255, verbose_name='App Name')),
                ('deep_link_prefix', models.CharField(blank=True, default='', max_length=255, verbose_name='Deep link prefix')),
                ('maintenance_mode', models.BooleanField(default=False, verbose_name='Maintenance mode')),
                ('app_version', models.CharField(default='1.0.0', max_length=100, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: 111.222.333 ', regex='^(\\d+)\\.(\\d+)(?:\\.(\\d+))?(?:\\-(\\w+))?$')], verbose_name='App Version')),
                ('app_version_bundle', models.PositiveIntegerField(default=1, verbose_name='app version bundle')),
                ('last_bundle_version', models.PositiveIntegerField(default=1, verbose_name='Last bundle version')),
                ('minimum_supported_bundle_version', models.PositiveIntegerField(default=1, verbose_name='minimum supported bundle version')),
                ('by_pass_sms', models.BooleanField(default=False, verbose_name='by pass sms')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CorrectPredictScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('arrange_score', models.PositiveIntegerField(default=1, verbose_name='arrange score')),
                ('change_player_score', models.PositiveIntegerField(default=1, verbose_name='change player score')),
                ('goal_score', models.PositiveIntegerField(default=1, verbose_name='goal score')),
                ('yellow_card_score', models.PositiveIntegerField(default=1, verbose_name='yellow card score')),
                ('red_card_score', models.PositiveIntegerField(default=1, verbose_name='red_card score')),
                ('correct_winner_score', models.PositiveIntegerField(default=1, verbose_name='correct winner score')),
                ('final_result_score', models.PositiveIntegerField(default=1, verbose_name='final result score')),
                ('assist_goal_score', models.PositiveIntegerField(default=1, verbose_name='assist goal score')),
                ('best_player_score', models.PositiveIntegerField(default=1, verbose_name='best player score')),
                ('penalty_score', models.PositiveIntegerField(default=1, verbose_name='penalty score')),
                ('arrange_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='arrange negative score')),
                ('change_player_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='change player negative score')),
                ('goal_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='goal negative score')),
                ('yellow_card_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='yellow card negative score')),
                ('red_card_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='red_card negative score')),
                ('correct_winner_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='correct winner negative score')),
                ('final_result_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='final result negative score')),
                ('assist_goal_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='assist goal negative score')),
                ('best_player_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='best player negative score')),
                ('penalty_negative_score', models.IntegerField(default=-1, validators=[django.core.validators.MaxValueValidator(0)], verbose_name='penalty negative score')),
            ],
            options={
                'verbose_name': 'Correct Predict Score',
                'verbose_name_plural': 'Correct Predict Scores',
            },
        ),
    ]
