from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import SignUpForm, DailyForm
from .models import User, InternProfile, DailyReport
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .pdf import generate_pdf


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


@login_required
def intern_home(request):
    # Handle intern's home page
    try:
        intern_profile = request.user.internprofile
        department = intern_profile.department
        supervisor = intern_profile.supervisor
        daily_reports = intern_profile.dailyreport_set.all()
    except InternProfile.DoesNotExist:
        return redirect('default_page')

    # Handle daily report form submission
    if request.method == 'POST':
        form = DailyForm(request.POST)
        if form.is_valid():
            daily_report = form.save(commit=False)
            daily_report.intern = intern_profile
            daily_report.save()
            return redirect('intern_home')  # Prevent duplicate submissions
    else:
        form = DailyForm()

    return render(request, 'intern_home.html', {
        'intern_profile': intern_profile,
        'department': department,
        'supervisor': supervisor,
        'daily_reports': daily_reports,
        'form': form,
    })


@login_required
def supervisor_home(request):
    # Render supervisor's home page
    return render(request, 'supervisor_home.html')


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
