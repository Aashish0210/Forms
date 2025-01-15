# Generated by Django 5.1.4 on 2025-01-15 06:47

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('pu_reg_no', models.CharField(default='1-12-2024', max_length=20)),
                ('role', models.CharField(choices=[('intern', 'Intern'), ('supervisor', 'Supervisor')], default='intern', max_length=20)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('phone_no', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_set', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=200)),
                ('head', models.ForeignKey(limit_choices_to=models.Q(('role', 'department_head')), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_head', to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ManyToManyField(limit_choices_to=models.Q(('role', 'supervisor')), related_name='supervised_departments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('pu_reg_no', models.CharField(max_length=20, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interns', to='usermanagement.department')),
                ('supervisor', models.ForeignKey(limit_choices_to=models.Q(('role', 'supervisor')), null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='interns', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(limit_choices_to=models.Q(('role', 'intern')), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField()),
                ('task_done', models.TextField()),
                ('problem_faced', models.TextField()),
                ('intern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usermanagement.internprofile')),
            ],
            options={
                'verbose_name': 'Intern Evaluation Form',
                'verbose_name_plural': 'Intern Evaluation Forms',
            },
        ),
        migrations.CreateModel(
            name='SupervisorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('phone_no', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('user', models.OneToOneField(limit_choices_to=models.Q(('role', 'supervisor')), on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectManagementForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('current_status', models.CharField(choices=[('Completed', 'Completed'), ('Incomplete', 'Incomplete'), ('User Input', 'User Input')], max_length=50)),
                ('progress', models.DecimalField(decimal_places=2, max_digits=5)),
                ('priority_level', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=50)),
                ('milestone_achievement', models.TextField(blank=True, null=True)),
                ('next_milestone', models.TextField(blank=True, null=True)),
                ('risk_and_challenges', models.TextField()),
                ('client_or_stakeholder', models.CharField(max_length=255)),
                ('tools_and_technology', models.CharField(max_length=255)),
                ('custom_tool', models.CharField(blank=True, max_length=255)),
                ('project_manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usermanagement.supervisorprofile')),
                ('team_member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_members', to='usermanagement.supervisorprofile')),
            ],
        ),
    ]
