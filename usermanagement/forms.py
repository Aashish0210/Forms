from django import forms
from .models import User, InternProfile, SupervisorProfile, Department, DailyReport,ProjectManagementForm,DailyActivity, NextDayPlanning
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import TimeInput


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'})
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'})
    )
    role = forms.ChoiceField(
        choices=User.ROLES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    phone_no = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'})
    )
    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='supervisor'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    email = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'})
    )
    pu_reg_no = forms.CharField(
        required=False,  # Make the field optional
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'PU Registration Number'})
    )

    class Meta:
        model = User  # Ensure this points to your custom User model
        fields = [
            'role', 'username', 'first_name', 'last_name', 'email', 'phone_no', 
            'department', 'password1', 'password2', 'pu_reg_no'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.phone_no = self.cleaned_data.get('phone_no')  # Optionally save phone number
        
        if commit:
            user.save()

        # Create or update related profiles
        if user.role == 'intern':
            InternProfile.objects.create(
                user=user, 
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone_no=user.phone_no,
                department=self.cleaned_data.get('department'),
                pu_reg_no=self.cleaned_data.get('pu_reg_no'),
                supervisor=self.cleaned_data.get('supervisor'), 
            )

        if user.role == 'supervisor':
            SupervisorProfile.objects.create(
                user=user, 
                first_name=user.first_name,
                last_name=user.last_name,
                phone_no=self.cleaned_data.get('phone_no'),
                email=self.cleaned_data.get('email'),
                department=user.department
            )

        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User  # Your custom User model
        fields = ['username', 'password']




class DateInput(forms.DateInput):
    input_type = 'date'  # HTML5 date input

class TimeInput(forms.TimeInput):
    input_type = 'time'  # HTML5 time input

class DailyForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['date', 'time_in', 'time_out', 'task_done', 'problem_faced']
        widgets = {
            'date': DateInput(attrs={'class': 'form-control'}),  # Add a calendar picker
            'time_in': TimeInput(attrs={'class': 'form-control'}),
            'time_out': TimeInput(attrs={'class': 'form-control'}),
            'task_done': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'problem_faced': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class DailyActivityForm(forms.ModelForm):
    class Meta:
        model = DailyActivity
        fields = [
            'date','start_time', 'end_time', 
            'total_hours', 'activity', 'remarks', 'other_remarks'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'activity': forms.Textarea(attrs={'rows': 3}),
            'other_remarks': forms.Textarea(attrs={'rows': 3}),
        }


class NextDayPlanningForm(forms.ModelForm):
    class Meta:
        model = NextDayPlanning
        fields = [
             'date','coordination', 'start_time', 'end_time', 
            'total_hours', 'to_do'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'coordination': forms.Textarea(attrs={'rows': 3}),
            'to_do': forms.Textarea(attrs={'rows': 3}),
        }


class InternProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='intern'),
        widget=forms.TextInput(attrs={'class': 'autocomplete'})
    )
    supervisor = forms.ModelChoiceField(
        queryset=User.objects.filter(role='supervisor'),
        required=False
    )
    phone_no = forms.CharField(
        max_length=15, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'phone-input'})
    )

    class Meta:
        model = InternProfile
        fields = ['user', 'first_name', 'last_name', 'email', 'pu_reg_no', 'phone_no', 'supervisor', 'department']


class SupervisorProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='supervisor'),
        widget=forms.TextInput(attrs={'class': 'autocomplete'})
    )

    class Meta:
        model = SupervisorProfile
        fields = ['user', 'phone_no', 'email']


class ProjectManagementFormForm(forms.ModelForm):
    class Meta:
        model = ProjectManagementForm
        fields = [
            'project_name', 'project_manager', 'team_member', 
            'start_date', 'end_date', 'current_status', 'progress', 
            'priority_level','milestone_achievement','next_milestone',
            'risk_and_challenges', 'client_or_stakeholder', 'tools_and_technology', 
            'custom_tool'
        ]
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Project Name'}),
            'project_manager': forms.Select(attrs={'class': 'form-select'}),
            'team_member': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter Team Members'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'current_status': forms.Select(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Current Status'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Progress (%)'}),
            'priority_level': forms.Select(attrs={'class': 'form-select'}),
            'milestone_achievement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achievements'}),
            'next_milestone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Next Milestone'}),
            'risk_and_challenges': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Risks and Challenges'}),
            'client_or_stakeholder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Client or Stakeholder'}),
            'tools_and_technology': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tools and Technology'}),
            'custom_tool': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Custom Tool'}),
        }


class DepartmentForm(forms.ModelForm):
    supervisor = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='supervisor'),
        widget=forms.CheckboxSelectMultiple  # Allow selecting multiple supervisors
    )

    class Meta:
        model = Department
        fields = ['name', 'head', 'supervisor', 'location']


# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile
#         fields = ['file']