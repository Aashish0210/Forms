from django import forms
from .models import User, InternProfile, SupervisorProfile, Department, DailyReport
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import TimeInput


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'})
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
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'PU Registration Number'})
    )
    
    class Meta:
        model = User  # Ensure this points to your custom User model
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'password1', 'password2', 'role', 'phone_no', 'pu_reg_no'
        ]  # Include additional fields here if necessary

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
                pu_reg_no=self.cleaned_data.get('pu_reg_no'),
                supervisor=self.cleaned_data.get('supervisor'), 
                department=self.cleaned_data.get('department')
            )

        if user.role == 'supervisor':
            SupervisorProfile.objects.create(
                user=user, 
                first_name=user.first_name,
                last_name=user.last_name,
                phone_no=self.cleaned_data.get('phone_no'),
                email=self.cleaned_data.get('email')
            )

        return user


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User  # Your custom User model
        fields = ['username', 'password']


class DailyForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        fields = ['time_in', 'time_out', 'task_done', 'problem_faced']
        widgets = {
            'time_in': TimeInput(attrs={'type': 'time'}),
            'time_out': TimeInput(attrs={'type': 'time'}),
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


class DepartmentForm(forms.ModelForm):
    supervisor = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='supervisor'),
        widget=forms.CheckboxSelectMultiple  # Allow selecting multiple supervisors
    )

    class Meta:
        model = Department
        fields = ['name', 'head', 'supervisor', 'location']
