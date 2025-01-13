from django.contrib import admin
from .models import User, InternProfile, SupervisorProfile, Department,DailyReport

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','phone_no', 'role', 'email', 'is_active','pu_reg_no')  # Customize list display
    list_filter = ('role', 'is_active')  # Filter by role and active status
    search_fields = ('username', 'email')  # Searchable fields
    
class DailyReportInline(admin.TabularInline):
    model = DailyReport
    extra = 0  # This will add one extra empty form for a new daily report
    fields = ['time_in', 'time_out', 'task_done', 'problem_faced']  # Define the fields you want to show

# Admin for InternProfile
class InternProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'supervisor', 'department','first_name','last_name','phone_no','email',)
    list_filter = ('department',)
    search_fields = ('user__username','first_name','last_name','phone_no','email', 'supervisor__username', 'department__name')
    inlines = [DailyReportInline] # Search by related fields
    
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_no')  # Customize list display for supervisor profiles
    search_fields = ('user__username', 'phone_no')  # Search by supervisor username and phone number

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head')  # Customize list display for departments
    search_fields = ('name', 'head__username')  # Search by department name and head's username
    list_filter = ('head',)  # Filter by department head

# Register the models with their respective admin classes
admin.site.register(User, UserAdmin)
admin.site.register(InternProfile, InternProfileAdmin)
admin.site.register(SupervisorProfile, SupervisorProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
