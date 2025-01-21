from django import forms
from .models import User, InternProfile, SupervisorProfile, Department, DailyReport,ProjectManagementForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import TimeInput
from .models import InternDailyActivity, InternNextDayPlanning, SupervisorDailyActivity, SupervisorNextDayPlanning


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
                # intern_st_date=user.intern_st_date,
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

from django import forms
from django.core.exceptions import ValidationError
from .models import DailyReport

class DailyForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['date', 'time_in', 'time_out', 'task_done', 'total_hours', 'problem_faced']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Add a calendar picker
            'time_in': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'time_out': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'task_done': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'total_hours': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': ' Total hours will be automatically filled '
            }),
            'problem_faced': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        time_in = cleaned_data.get('time_in')
        time_out = cleaned_data.get('time_out')

        if time_in and time_out:
            # Ensure time_out is later than time_in
            if time_out <= time_in:
                raise ValidationError("Time out must be later than time in.")

            # Calculate  Total hours will be automatically filled
            total_seconds = (time_out.hour * 3600 + time_out.minute * 60) - (time_in.hour * 3600 + time_in.minute * 60)
            total_hours = round(total_seconds / 3600, 2)  # Convert to hours, rounded to 2 decimal places

            # Update total_hours field
            cleaned_data['total_hours'] = total_hours

        return cleaned_data


class InternDailyActivityForm(forms.ModelForm):
    class Meta:
        model = InternDailyActivity
        fields = ['intern_profile', 'date', 'start_time', 'end_time', 'total_hours', 'activity', 'remarks', 'other_remarks']
        widgets = {
            'intern_profile': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' Total hours will be automatically filled'}),
            'activity': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Activity Details'}),
            'remarks': forms.Select(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarks'}),
            'other_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Other Remarks'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be later than start time.")
            
            # Calculate  Total hours will be automatically filled
            total_seconds = (end_time.hour * 3600 + end_time.minute * 60) - (start_time.hour * 3600 + start_time.minute * 60)
            total_hours = round(total_seconds / 3600, 2)
            cleaned_data['total_hours'] = total_hours

        return cleaned_data


class InternNextDayPlanningForm(forms.ModelForm):
    class Meta:
        model = InternNextDayPlanning
        fields = ['intern_profile', 'date', 'coordination', 'start_time', 'end_time', 'total_hours', 'to_do']
        widgets = {
            'intern_profile': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'coordination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Coordination Details'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' Total hours will be automatically filled'}),
            'to_do': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'To-Do Details'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be later than start time.")
            
            # Calculate  Total hours will be automatically filled
            total_seconds = (end_time.hour * 3600 + end_time.minute * 60) - (start_time.hour * 3600 + start_time.minute * 60)
            total_hours = round(total_seconds / 3600, 2)
            cleaned_data['total_hours'] = total_hours

        return cleaned_data



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


class SupervisorDailyActivityForm(forms.ModelForm):
    class Meta:
        model = SupervisorDailyActivity
        fields = ['supervisor_profile', 'date', 'start_time', 'end_time', 'total_hours', 'activity', 'remarks', 'other_remarks']
        widgets = {
            'supervisor_profile': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' Total hours will be automatically filled'}),
            'activity': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Activity Details'}),
            'remarks': forms.Select(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Remarks'}),
            'other_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Other Remarks'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be later than start time.")
            
            # Calculate  Total hours will be automatically filled
            total_seconds = (end_time.hour * 3600 + end_time.minute * 60) - (start_time.hour * 3600 + start_time.minute * 60)
            total_hours = round(total_seconds / 3600, 2)
            cleaned_data['total_hours'] = total_hours

        return cleaned_data


class SupervisorNextDayPlanningForm(forms.ModelForm):
    class Meta:
        model = SupervisorNextDayPlanning
        fields = ['supervisor_profile', 'date', 'coordination', 'start_time', 'end_time', 'total_hours', 'to_do']
        widgets = {
            'supervisor_profile': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'coordination': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Coordination Details'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'total_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ' Total hours will be automatically filled'}),
            'to_do': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'To-Do Details'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be later than start time.")
            
            # Calculate  Total hours will be automatically filled
            total_seconds = (end_time.hour * 3600 + end_time.minute * 60) - (start_time.hour * 3600 + start_time.minute * 60)
            total_hours = round(total_seconds / 3600, 2)
            cleaned_data['total_hours'] = total_hours

        return cleaned_data


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
            'project_manager': forms.Select(attrs={'class': 'form-control'}),  # Updated class
            'team_member': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter Team Members'}),  # Updated class
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Updated class
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),  # Updated class
            'current_status': forms.Select(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Current Status'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Progress (%)'}),
            'priority_level': forms.Select(attrs={'class': 'form-control'}),  # Updated class
            'milestone_achievement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Achievements'}),
            'next_milestone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Next Milestone'}),
            'risk_and_challenges': forms.Textarea(attrs={'class': 'form-control textarea', 'rows': 3, 'placeholder': 'Risks and Challenges'}),
            'client_or_stakeholder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Client or Stakeholder'}),
            'tools_and_technology': forms.Textarea(attrs={'class': 'form-control textarea', 'rows': 3, 'placeholder': 'Tools and Technology'}),
            'custom_tool': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Custom Tool'}),
        }



class DepartmentForm(forms.ModelForm):
    supervisor = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='supervisor'),
        widget=forms.CheckboxSelectMultiple  # Allow selecting multiple supervisors
    )

    class Meta:
        model = Department
        fields = ['name', 'head', 'supervisor', 'name_and_location']


# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = UploadedFile
#         fields = ['file']