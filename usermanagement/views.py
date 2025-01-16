from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import  DailyForm,ProjectManagementFormForm,SignUpForm
from .models import User, InternProfile, DailyReport,SupervisorProfile
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .pdf import generate_pdf
import os
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib import messages

# from .forms import UploadFileForm
# from .models import UploadedFile


def send_email_with_attachment(file_path):
    email = EmailMessage(
        subject="Generated PDF Report",
        body="Please find the attached PDF report.",
        from_email=settings.EMAIL_HOST_USER,
        to=['frontdesksera@gmail.com'],  # Recipient email
    )
    email.attach_file(file_path)
    email.send()


@staff_member_required
def superuser_dashboard(request):
    # Fetch all intern profiles to display on the superuser dashboard
    interns = InternProfile.objects.all()
    return render(request, 'superuser_dashboard.html', {'interns': interns})



def signup(request):
    # Handle user sign-up
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in after signup
            return redirect('redirect_to_role_home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def custom_login(request):
    # Handle custom login form
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('redirect_to_role_home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def redirect_to_role_home(request):
    # Redirect user based on their role to the respective homepage
    if request.user.role == 'intern':
        return redirect('intern_home')
    elif request.user.role == 'supervisor':
        return redirect('supervisor_home')
    elif request.user.role == 'department_head':
        return redirect('department_home')
    elif request.user.is_superuser:
        return redirect('superuser_dashboard')
    return redirect('default_page')


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DailyForm, InternDailyActivityForm, InternNextDayPlanningForm
from .models import InternProfile
import logging

# Create a logger instance
logger = logging.getLogger(__name__)

@login_required
def intern_home(request):
    try:
        # Retrieve the intern's profile
        intern_profile = request.user.internprofile
        department = intern_profile.department
        supervisor = intern_profile.supervisor

        # Fetch related data for display
        daily_reports = intern_profile.dailyreport_set.all()
        daily_activities = intern_profile.interndailyactivity_set.all()
        next_day_plans = intern_profile.internnextdayplanning_set.all()
    except InternProfile.DoesNotExist:
        logger.error("InternProfile not found for the logged-in user.")
        return redirect('default_page')

    # Initialize forms
    daily_report_form = DailyForm()
    daily_activity_form = InternDailyActivityForm()
    next_day_planning_form = InternNextDayPlanningForm()

    # Handle POST requests for form submissions
    if request.method == 'POST':
        if 'daily_report' in request.POST:
            daily_report_form = DailyForm(request.POST)
            if daily_report_form.is_valid():
                daily_report = daily_report_form.save(commit=False)
                daily_report.intern = intern_profile
                daily_report.save()
                messages.success(request, "Daily Report submitted successfully!")
                logger.info("Daily Report submitted successfully.")
            else:
                messages.error(request, "Failed to submit Daily Report. Please check the form and try again.")
                logger.error(f"Daily Report Form Errors: {daily_report_form.errors}")

        elif 'daily_activity' in request.POST:
            daily_activity_form = InternDailyActivityForm(request.POST)
            if daily_activity_form.is_valid():
                daily_activity = daily_activity_form.save(commit=False)
                daily_activity.intern_profile = intern_profile  # Adjust field as per model definition
                daily_activity.save()
                messages.success(request, "Daily Activity submitted successfully!")
                logger.info("Daily Activity submitted successfully.")
            else:
                messages.error(request, "Failed to submit Daily Activity. Please check the form and try again.")
                logger.error(f"Daily Activity Form Errors: {daily_activity_form.errors}")

        elif 'next_day_planning' in request.POST:
            next_day_planning_form = InternNextDayPlanningForm(request.POST)
            if next_day_planning_form.is_valid():
                next_day_planning = next_day_planning_form.save(commit=False)
                next_day_planning.intern_profile = intern_profile  # Adjust field as per model definition
                next_day_planning.save()
                messages.success(request, "Next Day Planning submitted successfully!")
                logger.info("Next Day Planning submitted successfully.")
            else:
                messages.error(request, "Failed to submit Next Day Planning. Please check the form and try again.")
                logger.error(f"Next Day Planning Form Errors: {next_day_planning_form.errors}")

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


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import (
    ProjectManagementFormForm, 
    SupervisorDailyActivityForm, 
    SupervisorNextDayPlanningForm
)
from .models import SupervisorProfile

@login_required
def supervisor_home(request):
    try:
        # Retrieve supervisor profile
        supervisor_profile = request.user.supervisorprofile
        managed_projects = supervisor_profile.projectmanagementform_set.all()
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
def department_home(request):
    # Render department head's home page
    return render(request, 'department_home.html')


@login_required
def superuser_home(request):
    # Render superuser's dashboard
    return render(request, 'superuser_dashboard.html')


@login_required
def user_logout(request):
    # Log out the user and redirect to the default page
    logout(request)
    return redirect('default_page')


def default_page(request):
    # Render the default page for users not logged in or other cases
    return render(request, 'default.html')
