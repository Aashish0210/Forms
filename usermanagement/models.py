from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Q
from django.utils.timezone import now


# -------------------------------------------
# User Model
# -------------------------------------------
class User(AbstractUser):
    ROLES = [
        ('intern', 'Intern'),
        ('supervisor', 'Supervisor'),
    ]
    pu_reg_no = models.CharField(max_length=20, default="1-12-2024")
    role = models.CharField(max_length=20, choices=ROLES, default='intern')
    phone_no = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Avoid conflicts with default User model
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True
    )

    def __str__(self):
        return f"{self.username} - {self.role}"


# -------------------------------------------
# Department Model
# -------------------------------------------
class Department(models.Model):
    name = models.CharField(max_length=50)
    head = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='department_head',
        limit_choices_to=Q(role='supervisor')  # Restrict to supervisors
    )
    location = models.CharField(max_length=200)
    supervisors = models.ManyToManyField(
        User,
        related_name='supervised_departments',
        limit_choices_to=Q(role='supervisor')
    )

    def __str__(self):
        return self.name


# -------------------------------------------
# Supervisor Profile
# -------------------------------------------
class SupervisorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(role='supervisor')
    )
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"Supervisor: {self.user.username}"


# -------------------------------------------
# Intern Profile
# -------------------------------------------
class InternProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(role='intern')
    )
    first_name=models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    pu_reg_no = models.CharField(max_length=20, null=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    supervisor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='interns',
        limit_choices_to=Q(role='supervisor')
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        related_name='interns'
    )
    email = models.EmailField(max_length=100)

    def __str__(self):
        department_name = self.department.name if self.department else 'No Department'
        return f"Intern: {self.user.username}, Department: {department_name}"


# -------------------------------------------
# Project Management Form
# -------------------------------------------
class ProjectManagementForm(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Incomplete', 'Incomplete'),
        ('User Input', 'User Input'),
    ]
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    project_name = models.CharField(max_length=255)
    project_manager = models.ForeignKey(SupervisorProfile, on_delete=models.SET_NULL, null=True)
    team_member = models.ForeignKey(SupervisorProfile, related_name='team_members', on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    progress = models.DecimalField(max_digits=5, decimal_places=2)
    priority_level = models.CharField(max_length=50, choices=PRIORITY_CHOICES)
    milestone_achievement = models.TextField(blank=True, null=True)
    next_milestone = models.TextField(blank=True, null=True)
    risk_and_challenges = models.TextField()
    client_or_stakeholder = models.CharField(max_length=255)
    tools_and_technology = models.CharField(max_length=255)
    custom_tool = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.project_name


# -------------------------------------------
# Daily Activity and Next Day Planning
# -------------------------------------------
class DailyActivity(models.Model):
    intern_profile = models.ForeignKey(InternProfile, null=True, blank=True, on_delete=models.CASCADE)
    supervisor_profile = models.ForeignKey(SupervisorProfile, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    activity = models.TextField()
    remarks = models.CharField(max_length=20, choices=[("Completed", "Completed"), ("Uncompleted", "Uncompleted"), ("Other", "Other")])
    other_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        # Safely check if intern_profile or supervisor_profile exists
        intern_username = self.intern_profile.user.username if self.intern_profile and self.intern_profile.user else "No Intern"
        supervisor_username = self.supervisor_profile.user.username if self.supervisor_profile and self.supervisor_profile.user else "No Supervisor"
        
        # Return formatted string based on available profiles
        return f"{intern_username if self.intern_profile else supervisor_username} - {self.date}"


class NextDayPlanning(models.Model):
    intern_profile = models.ForeignKey(InternProfile, null=True, blank=True, on_delete=models.CASCADE)
    supervisor_profile = models.ForeignKey(SupervisorProfile, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    coordination = models.TextField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    to_do = models.TextField()

    def __str__(self):
        # Safely check if intern_profile or supervisor_profile exists
        intern_username = self.intern_profile.user.username if self.intern_profile and self.intern_profile.user else "No Intern"
        supervisor_username = self.supervisor_profile.user.username if self.supervisor_profile and self.supervisor_profile.user else "No Supervisor"
        
        # Return formatted string based on available profiles
        return f"{intern_username if self.intern_profile else supervisor_username} - {self.date} Planning"


# -------------------------------------------
# Intern Daily Report
# -------------------------------------------
class DailyReport(models.Model):
    intern = models.ForeignKey(InternProfile, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()
    task_done = models.TextField()
    problem_faced = models.TextField()

    def __str__(self):
        return f"Daily Report for {self.intern.user.username} on {self.date}"

    class Meta:
        verbose_name = "Intern Evaluation Form"
        verbose_name_plural = "Intern Evaluation Forms"
