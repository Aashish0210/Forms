# Generated by Django 5.1.4 on 2025-01-16 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0010_supervisorprofile_department'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supervisorprofile',
            name='department',
        ),
    ]
