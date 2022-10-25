# Generated by Django 4.1.2 on 2022-10-25 06:19

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_predictionarrange_is_penalty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='predictionarrange',
            name='point',
            field=models.PositiveIntegerField(blank=True, help_text='Points earned from correct predictions.', null=True, verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='player',
            name='avatar',
            field=models.JSONField(blank=True, default=user.models.Player.get_avatar, null=True, verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default=user.models.User.generate_token, max_length=255, null=True, verbose_name='Token'),
        ),
    ]