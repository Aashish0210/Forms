from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from django.core.validators import RegexValidator
from django.conf import settings



# -------------------------------------------
# User Model
# -------------------------------------------
class User(AbstractUser):
    ROLES = [
        ('intern', 'Intern'),
        ('supervisor', 'Supervisor'),
        ('employee', 'employee'),
        ('students', 'Students'),
        ('superuser', 'Superuser'),
    ]
    pu_reg_no = models.CharField(max_length=20,null='True', blank=True)
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
    department = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        if self.role in ['intern', 'supervisor', 'employee']:
            return f"{self.username} - {self.role}"
        return f"{self.username} - Other Role"

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
    name_and_location = models.CharField(max_length=200)
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
        limit_choices_to=Q(role='supervisor')  # Restrict to supervisors
    )
    first_name = models.CharField(max_length=150, blank=True)  # Allows blank values
    last_name = models.CharField(max_length=150, blank=True)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"Supervisor: {self.user.username}"

    def delete(self, *args, **kwargs):
        # Delete associated User (Supervisor) after deleting the profile
        user = self.user
        super().delete(*args, **kwargs)  # First, delete the profile
        user.delete()  # Then, delete the user
        print(f"Supervisor {user.username} and associated profile deleted.")

# -------------------------------------------
# Intern Profile
# -------------------------------------------

class InternProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(role='intern')
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    pu_reg_no = models.CharField(max_length=20, null=True,blank=True)
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
    
    def delete(self, *args, **kwargs):
        # Delete associated User (Intern)
        user = self.user
        super().delete(*args, **kwargs)  # First, delete the profile
        user.delete()  # Then, delete the user
        print(f"Intern {user.username} and associated profile deleted.")

class Students(models.Model):
    username=models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(role='students')
    )
    img_field = models.CharField(max_length=200, blank=True, null=True, help_text="Enter a valid image URL.")
    full_name=models.CharField(max_length=20)
    gender = models.CharField(
        max_length=20,
        choices=[
            ('male', 'Male'),
            ('female', 'Female')
        ],
        default='male'
    )
    date_of_birth=models.DateField()
    phone_no = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ],
        help_text="Enter phone number in international format, e.g., +123456789."
    )
    email=models.EmailField(max_length=255)
    parents_info=models.CharField(max_length=200,default={'Father Name=Hari', 'Mother Name=Sita'})
    par_phone_no=models.CharField(max_length=15)
    def __str__(self):
        return f"{self.full_name} - {self.parents_info}"


# -------------------------------------------
# Employee Profile
# -------------------------------------------


class EmployesProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to=Q(role='Employee'),
        related_name='employee_profile'  # Add related_name for easier access
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"Employee: {self.user.username}"

# -------------------------------------------
#        Form section for different Profiles
# -------------------------------------------



# -------------------------------------------
# Intern Daily Report
# -------------------------------------------
class DailyReport(models.Model):
    intern = models.ForeignKey(InternProfile, on_delete=models.CASCADE,limit_choices_to={'user': settings.AUTH_USER_MODEL},)
    date = models.DateField()
    start_time = models.TimeField(default='10:30:AM')
    end_time = models.TimeField(default='05:00:PM')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    task_done = models.TextField()
    problem_faced = models.TextField()

    def __str__(self):
        return f"Daily Report for {self.intern.user.username} on {self.date}"

    class Meta:
        verbose_name = "Intern Evaluation Form"
        verbose_name_plural = "Intern Evaluation Forms"




# -------------------------------------------
# Daily Activity and Next Day Planning for Intern
# -------------------------------------------
class InternDailyActivity(models.Model):
    intern_profile = models.ForeignKey(InternProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    start_time = models.TimeField(default='10:30:AM')
    end_time = models.TimeField(default='05:00:PM')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    activity = models.TextField()
    remarks = models.CharField(max_length=20, choices=[("Completed", "Completed"), ("Uncompleted", "Uncompleted"), ("Other", "Other")])
    other_remarks = models.TextField(blank =True, null=True)

    def __str__(self):
        return f"{self.intern_profile.user.username} - {self.date}"


# -------------------------------------------
# Next Day Planning for Intern
# -------------------------------------------
class InternNextDayPlanning(models.Model):
    intern_profile = models.ForeignKey(InternProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    coordination = models.TextField()
    start_time = models.TimeField(default='10:30:AM')
    end_time = models.TimeField(default='05:00:PM')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    to_do = models.TextField()

    def __str__(self):
        return f"{self.intern_profile.user.username} - {self.date} Planning"
    



# -------------------------------------------
# Project Management Form for supervisor
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

    project_manager = models.ForeignKey(
        'SupervisorProfile', 
        on_delete=models.CASCADE,  # Change to CASCADE for deletion of the associated form
        null=True, 
        related_name='supervised_projects'
    )
    team_member = models.ManyToManyField(
        User, 
        blank=True, 
        related_name='team_member_projects'
    )
    project_name = models.CharField(max_length=255)
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
        return f"Project Management form for {self.project_name}"


# -------------------------------------------
# Daily Activity for Supervisor
# -------------------------------------------
class SupervisorDailyActivity(models.Model):
    supervisor_profile = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    start_time = models.TimeField(default='10:30:AM')
    end_time = models.TimeField(default='05:00:PM')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    activity = models.TextField()
    remarks = models.CharField(max_length=20, choices=[("Completed", "Completed"), ("Uncompleted", "Uncompleted"), ("Other", "Other")])
    other_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.supervisor_profile.user.username} - {self.date}"


# -------------------------------------------
# Next Day Planning for Supervisor
# -------------------------------------------
class SupervisorNextDayPlanning(models.Model):
    supervisor_profile = models.ForeignKey(SupervisorProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    coordination = models.TextField()
    start_time = models.TimeField(default='10:30:AM')
    end_time = models.TimeField(default='05:00:PM')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    to_do = models.TextField()

    def __str__(self):
        return f"{self.supervisor_profile.user.username} - {self.date} Planning"



# -------------------------------------------
#Academic Details for Students
# -------------------------------------------

class StudentAcademicDetails(models.Model):
    user=models.ForeignKey(Students,on_delete=models.CASCADE)
    degree=models.CharField(max_length=30)
    started_date=models.DateField()
    division_gpa = models.CharField(max_length=100, blank=True, null=True, help_text="Enter the division or GPA as a string.")
    college_university=models.CharField(max_length=30)
    

class PermanentAddress(models.Model):
    user=models.ForeignKey(Students,on_delete=models.CASCADE)
    provience=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    mc_rm=models.CharField(max_length=30,help_text="Enter the name of metropolitan/district name")
    ward_no=models.IntegerField()

class CurrentAddress(models.Model):
    user=models.ForeignKey(Students,on_delete=models.CASCADE)
    provience=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    mc_rm=models.CharField(max_length=30,help_text="Enter the name of metropolitan/district name")
    ward_no=models.IntegerField()

class IntrestedCourses(models.Model):
    user=models.ForeignKey(Students,on_delete=models.CASCADE)
    courses=[
        ('Accounting','Accounting'),
        ('Office Package','Office Package'),
        ('Graaphic design','Graaphic design'),
        ('Web Develpoment','Web Develpoment'),
        ('SEO','SEO'),
        ('English Language','English Language'),
        ('video Editing','video Editing'),
        ('Others','Others'),
    ]
    intrested_courses=models.CharField(max_length=30,choices=courses)
    suitable_time=models.CharField(max_length=30)


# -------------------------------------------
# Daily Activity for Employee
# -------------------------------------------
class EmployeeDailyActivity(models.Model):
    employee_profile = models.ForeignKey(EmployesProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    start_time = models.TimeField(default='10:30:AM')
    end_time = models.TimeField(default='05:00:PM')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    activity = models.TextField()
    remarks = models.CharField(max_length=20, choices=[("Completed", "Completed"), ("Uncompleted", "Uncompleted"), ("Other", "Other")])
    other_remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee_profile.user.username} - {self.date}"


# -------------------------------------------
# Next Day Planning for Supervisor
# -------------------------------------------
class EmployeeNextDayPlanning(models.Model):
    employee_profile = models.ForeignKey(EmployesProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    coordination = models.TextField()
    start_time = models.TimeField(default='10:30:AM')
    end_time = models.TimeField(default='05:00:PM')
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    to_do = models.TextField()

    def __str__(self):
        return f"{self.employee_profile.user.username} - {self.date} Planning"

