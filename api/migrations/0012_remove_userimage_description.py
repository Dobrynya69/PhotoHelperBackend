# Generated by Django 5.0.6 on 2024-06-07 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_userimagegroup_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userimage',
            name='description',
        ),
    ]
