from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Q


class User(AbstractUser):
    ROLES = [
        ('intern', 'Intern'),
        ('supervisor', 'Supervisor'),
        ('department_head', 'Department Head'),
        ('superuser', 'Superuser')
    ]

    pu_reg_no = models.CharField(max_length=20, default="1-12-2024")
    role = models.CharField(max_length=20, choices=ROLES, default='intern')
    first_name = models.CharField(max_length=150, blank=True)  # Allows blank values
    last_name = models.CharField(max_length=150, blank=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related name to avoid conflicts
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Custom related name to avoid conflicts
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"


class Department(models.Model):
    name = models.CharField(max_length=50)
    head = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='department_head',
        limit_choices_to=Q(role='department_head')  # Restrict to department heads
    )
    location = models.CharField(max_length=200)
    supervisor = models.ManyToManyField(
        User,
        related_name='supervised_departments',
        limit_choices_to=Q(role='supervisor')  # Restrict to supervisors
    )

    def __str__(self):
        return self.name


class SupervisorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(role='supervisor')  # Restrict to supervisors
    )
    first_name = models.CharField(max_length=150, blank=True)  # Allows blank values
    last_name = models.CharField(max_length=150, blank=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"Supervisor: {self.user.username}"


class InternProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(role='intern')  # Restrict to interns
    )
    first_name = models.CharField(max_length=150, blank=True)  # Allows blank values
    last_name = models.CharField(max_length=150, blank=True)
    pu_reg_no = models.CharField(max_length=20, default="1-12-2024")
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='interns',
        limit_choices_to=Q(role='supervisor')  # Restrict to supervisors
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='interns'
    )
    email = models.EmailField(max_length=100)  # Add email field if required

    def __str__(self):
        department_name = self.department.name if self.department else 'No Department'
        return f"Intern: {self.user.username}, Department: {department_name}"


class DailyReport(models.Model):
    intern = models.ForeignKey('InternProfile', on_delete=models.CASCADE)
    time_in = models.TimeField()
    time_out = models.TimeField()
    task_done = models.TextField()
    problem_faced = models.TextField()

    def __str__(self):
        return f"Daily Report for {self.intern.user.username}"
