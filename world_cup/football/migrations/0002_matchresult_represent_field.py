# Generated by Django 4.1.2 on 2022-11-10 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchresult',
            name='represent_field',
            field=models.JSONField(blank=True, null=True, verbose_name='represent field'),
        ),
    ]