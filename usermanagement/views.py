from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from datetime import datetime
from .pdf import generate_pdf
import logging
from django.contrib.auth.views import PasswordResetView

from .forms import (
    DailyForm, InternDailyActivityForm, InternNextDayPlanningForm,
    ProjectManagementFormForm, SupervisorDailyActivityForm,
    SupervisorNextDayPlanningForm, SignUpForm,EmployeeDailyActivityForm,EmployeeNextDayPlanningForm,BaseTimeForm

)
from .models import InternProfile, SupervisorProfile, DailyReport,EmployesProfile
# Logger Configuration
logger = logging.getLogger(__name__)

# Utility Function for Sending Email
def send_email_with_attachment(file_path):
    email = EmailMessage(
        subject="Generated PDF Report",
        body="Please find the attached PDF report.",
        from_email=settings.EMAIL_HOST_USER,
        to=['frontdesksera@gmail.com'],
    )
    email.attach_file(file_path)
    email.send()


# Authorization Utility
def check_role(user, role):
    return hasattr(user, 'role') and user.role == role

@login_required
def check_session(request):
    # If the user is authenticated, return session status as true
    return JsonResponse({'session_active': True})

def session_expired(request):
    # If session is expired or the user is not authenticated
    return JsonResponse({'session_active': False})


# Authentication and Authorization Views
def signup(request):
    """Handle user signup."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('redirect_to_role_home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def custom_login(request):
    """Custom login form."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('redirect_to_role_home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def redirect_to_role_home(request):
    """Redirect users to home based on role."""
    if request.user.is_superuser:
        return redirect('superuser_dashboard')
    elif check_role(request.user, 'intern'):
        return redirect('intern_home')
    elif check_role(request.user, 'employee'):
        return redirect('employee_home')
    elif check_role(request.user, 'supervisor'):
        return redirect('supervisor_home')
    elif check_role(request.user, 'department_head'):
        return redirect('department_home')
    return redirect('default_page')


@login_required
def user_logout(request):
    """Logout the user."""
    logout(request)
    return redirect('default_page')


# Intern Views
@login_required
@user_passes_test(lambda u: check_role(u, 'intern'), login_url='default_page')
def intern_home(request):
    try:
        intern_profile = request.user.internprofile
        department = intern_profile.department
        supervisor = intern_profile.supervisor

        daily_reports = intern_profile.dailyreport_set.all()  # Use related_name if defined
        daily_activities = intern_profile.interndailyactivity_set.all()
        next_day_plans = intern_profile.internnextdayplanning_set.all()
    except InternProfile.DoesNotExist:
        logger.error(f"InternProfile does not exist for user {request.user}.")
        return redirect('default_page')

    daily_report_form = DailyForm(request.POST or None)
    daily_activity_form = InternDailyActivityForm(request.POST or None)
    next_day_planning_form = InternNextDayPlanningForm(request.POST or None)

    if request.method == 'POST':
        if 'daily_report' in request.POST:
            handle_form_submission(request, daily_report_form, intern_profile, 'Daily Report')
        elif 'daily_activity' in request.POST:
            handle_form_submission(request, daily_activity_form, intern_profile, 'Daily Activity')
        elif 'next_day_planning' in request.POST:
            handle_form_submission(request, next_day_planning_form, intern_profile, 'Next Day Planning')

    return render(request, 'intern_home.html', {
        'intern_profile': intern_profile,
        'department': department,
        'supervisor': supervisor,
        'daily_reports': daily_reports,
        'daily_activities': daily_activities,
        'next_day_plans': next_day_plans,
        'daily_report_form': daily_report_form,
        'daily_activity_form': daily_activity_form,
        'next_day_planning_form': next_day_planning_form,
    })



# Supervisor Views

@login_required
def supervisor_home(request):
    try:
        # Retrieve supervisor profile
        supervisor_profile = request.user.supervisorprofile
        # Use the custom related_name for accessing managed projects
        managed_projects = supervisor_profile.supervised_projects.all()
        daily_activities = supervisor_profile.supervisordailyactivity_set.all()
        next_day_plans = supervisor_profile.supervisornextdayplanning_set.all()
    except SupervisorProfile.DoesNotExist:
        return redirect('default_page')


    # Initialize forms
    project_management_form = ProjectManagementFormForm()
    daily_activity_form = SupervisorDailyActivityForm()
    next_day_planning_form = SupervisorNextDayPlanningForm()

    # Handle POST requests
    if request.method == 'POST':
        if 'project_management' in request.POST:
            project_management_form = ProjectManagementFormForm(request.POST)
            if project_management_form.is_valid():
                project = project_management_form.save(commit=False)
                project.project_manager = supervisor_profile
                project.save()
                messages.success(request, "Project submitted successfully!")
                return redirect('supervisor_home')
            else:
                messages.error(request, "Could not submit project. Please try again.")

        elif 'daily_activity' in request.POST:
            daily_activity_form = SupervisorDailyActivityForm(request.POST)
            if daily_activity_form.is_valid():
                daily_activity = daily_activity_form.save(commit=False)
                daily_activity.supervisor_profile = supervisor_profile
                daily_activity.save()
                messages.success(request, "Daily Activity submitted successfully!")
                return redirect('supervisor_home')
            else:
                messages.error(request, "Could not submit Daily Activity. Please try again.")

        elif 'next_day_planning' in request.POST:
            next_day_planning_form = SupervisorNextDayPlanningForm(request.POST)
            if next_day_planning_form.is_valid():
                next_day_planning = next_day_planning_form.save(commit=False)
                next_day_planning.supervisor_profile = supervisor_profile
                next_day_planning.save()
                messages.success(request, "Next Day Planning submitted successfully!")
                return redirect('supervisor_home')
            else:
                messages.error(request, "Could not submit Next Day Planning. Please try again.")

    return render(request, 'supervisor_home.html', {
        'supervisor_profile': supervisor_profile,
        'managed_projects': managed_projects,
        'daily_activities': daily_activities,
        'next_day_plans': next_day_plans,
        'project_management_form': project_management_form,
        'daily_activity_form': daily_activity_form,
        'next_day_planning_form': next_day_planning_form,
    })

@login_required
def employee_home(request):
    try:
        # Retrieve the employee profile using the correct related_name
        employee_profile = request.user.employee_profile
        print(f"Employee Profile Retrieved: {employee_profile}")
        daily_activities = employee_profile.employeedailyactivity_set.all()
        next_day_plans = employee_profile.employeenextdayplanning_set.all()
    except EmployesProfile.DoesNotExist:
        print("EmployesProfile.DoesNotExist: Redirecting to default_page")
        return redirect('default_page')

    # Initialize forms
    daily_activity_form = EmployeeDailyActivityForm()
    next_day_planning_form = EmployeeNextDayPlanningForm()

    if request.method == 'POST':
        if 'daily_activity' in request.POST:
            daily_activity_form = EmployeeDailyActivityForm(request.POST)
            if daily_activity_form.is_valid():
                daily_activity = daily_activity_form.save(commit=False)
                daily_activity.employee_profile = employee_profile
                daily_activity.save()
                messages.success(request, "Daily Activity submitted successfully!")
                return redirect('employee_home')
            else:
                messages.error(request, "Could not submit Daily Activity. Please try again.")

        elif 'next_day_planning' in request.POST:
            next_day_planning_form = EmployeeNextDayPlanningForm(request.POST)
            if next_day_planning_form.is_valid():
                next_day_planning = next_day_planning_form.save(commit=False)
                next_day_planning.employee_profile = employee_profile
                next_day_planning.save()
                messages.success(request, "Next Day Planning submitted successfully!")
                return redirect('employee_home')
            else:
                messages.error(request, "Could not submit Next Day Planning. Please try again.")

    return render(request, 'employee_home.html', {
        'employee_profile': employee_profile,
        'daily_activities': daily_activities,
        'next_day_plans': next_day_plans,
        'daily_activity_form': daily_activity_form,
        'next_day_planning_form': next_day_planning_form,
    })


# Department Head Views
@login_required
@user_passes_test(lambda u: check_role(u, 'department_head'), login_url='default_page')
def department_home(request):
    """Department head's dashboard."""
    return render(request, 'department_home.html')


# Superuser Views
@staff_member_required
def superuser_dashboard(request):
    """Superuser dashboard."""
    interns = InternProfile.objects.all()
    return render(request, 'superuser_dashboard.html', {'interns': interns})


# Default Page for Unauthorized Access
def default_page(request):
    """Default page for unauthorized users."""
    return render(request, 'default.html')


# Helper Function for Form Handling
def handle_form_submission(request, form, intern_profile, form_name):
    """Helper to handle form submissions."""
    if form.is_valid():
        form_instance = form.save(commit=False)  # Don't save to the database yet
        form_instance.intern = intern_profile  # Set the foreign key field
        form_instance.save()  # Now save to the database
        messages.success(request, f"{form_name} submitted successfully!")
        logger.info(f"{form_name} submitted successfully.")
    else:
        messages.error(request, f"Failed to submit {form_name}. Please try again.")
        logger.error(f"{form_name} submission errors: {form.errors}.")

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, "Password reset email sent successfully.")
            return response
        except Exception as e:
            messages.error(self.request, "Error sending email: " + str(e))
            return redirect('password_reset')