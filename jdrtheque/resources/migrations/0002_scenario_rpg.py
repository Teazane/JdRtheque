# Generated by Django 4.1 on 2022-08-23 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario',
            name='rpg',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='resources.roleplaygame'),
        ),
    ]
