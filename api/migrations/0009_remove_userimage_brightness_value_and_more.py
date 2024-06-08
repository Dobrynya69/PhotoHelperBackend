# Generated by Django 5.0.6 on 2024-06-05 22:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_userimage_sharpness_value'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userimage',
            name='brightness_value',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='contrast_value',
        ),
        migrations.RemoveField(
            model_name='userimage',
            name='is_borderized',
        ),
        migrations.CreateModel(
            name='UserImageGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='userimage',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userimagegroup'),
        ),
        migrations.DeleteModel(
            name='ImageGroup',
        ),
    ]
