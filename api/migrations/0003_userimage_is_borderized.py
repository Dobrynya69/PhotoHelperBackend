# Generated by Django 5.0.1 on 2024-01-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_image_userimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='userimage',
            name='is_borderized',
            field=models.BooleanField(default=False),
        ),
    ]