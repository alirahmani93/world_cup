# Generated by Django 4.1.2 on 2022-10-22 20:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrectPredictScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='UUID')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='Updated time')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='Created time')),
                ('goal_score', models.PositiveIntegerField(default=1, verbose_name='goal score')),
                ('assist_goal_score', models.PositiveIntegerField(default=1, verbose_name='assist goal score')),
                ('yellow_card_score', models.PositiveIntegerField(default=1, verbose_name='yellow card score')),
                ('red_card_score', models.PositiveIntegerField(default=1, verbose_name='red_card score')),
                ('arrange_score', models.PositiveIntegerField(default=1, verbose_name='arrange score')),
                ('change_player_score', models.PositiveIntegerField(default=1, verbose_name='change player score')),
            ],
            options={
                'verbose_name': 'Correct Predict Score',
                'verbose_name_plural': 'Correct Predict Scores',
            },
        ),
    ]
