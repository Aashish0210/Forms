# Generated by Django 5.1.4 on 2025-01-16 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermanagement', '0011_remove_supervisorprofile_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supervisorprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='supervisorprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
