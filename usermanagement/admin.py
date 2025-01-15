from django.contrib import admin
from .models import User, InternProfile, SupervisorProfile, Department, DailyReport, ProjectManagementForm,DailyActivity,NextDayPlanning

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_no', 'role', 'email', 'is_active', 'pu_reg_no')  # Customize list display
    list_filter = ('role', 'is_active')  # Filter by role and active status
    search_fields = ('username', 'email')  # Searchable fields

class DailyReportInline(admin.TabularInline):
    model = DailyReport
    extra = 0  # This will add one extra empty form for a new daily report
    fields = ['date', 'time_in', 'time_out', 'task_done', 'problem_faced']   # Define the fields you want to 
    
class ProjectManagementFormInline(admin.TabularInline):
    model = ProjectManagementForm
    extra = 0
    fields = [ 'project_name', 'project_manager', 'team_member', 'start_date', 'end_date',
              'current_status', 'progress', 'priority_level', 'milestone_achievement', 'next_milestone',
              'risk_and_challenges', 'client_or_stakeholder', 'tools_and_technology', 'custom_tool']

    # Specify which ForeignKey to use with the 'fk_name' attribute
    fk_name = 'project_manager'  

class DailyActivityInline(admin.TabularInline):
    model = DailyActivity
    extra=0
    fields=[ 'date','start_time','end_time', 'total_hours','activity', 'remarks']

class NextDayPlanningInline(admin.TabularInline):
    model = NextDayPlanning
    extra=0
    fields=[ 'date','coordination','start_time','end_time', 'total_hours','to_do']

# Admin for InternProfile
class InternProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'supervisor', 'department', 'first_name', 'last_name', 'phone_no', 'email',)
    list_filter = ('department',)
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_no', 'email', 'supervisor__username', 'department__name')
    inlines = [DailyReportInline,DailyActivityInline,NextDayPlanningInline]  # Search by related fields

class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_no')  # Customize list display for supervisor profiles
    search_fields = ('user__username', 'phone_no')
    inlines = [ProjectManagementFormInline,DailyActivityInline,NextDayPlanningInline]  # Embed ProjectManagementForm inside the SupervisorProfile admin

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head')  # Customize list display for departments
    search_fields = ('name', 'head__username')  # Search by department name and head's username
    list_filter = ('head',)  # Filter by department head

# Register the models with their respective admin classes
admin.site.register(User, UserAdmin)
admin.site.register(InternProfile, InternProfileAdmin)
admin.site.register(SupervisorProfile, SupervisorProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
