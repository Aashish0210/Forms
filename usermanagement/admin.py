from django.contrib import admin
from .models import User, InternProfile, SupervisorProfile, Department
from .models import DailyReport, InternDailyActivity, InternNextDayPlanning, SupervisorDailyActivity, SupervisorNextDayPlanning
from .models import (ProjectManagementForm,
                     Students,
                     StudentAcademicDetails,
                     PermanentAddress,
                     CurrentAddress,
                     IntrestedCourses
                     )

# Admin for User Model
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_no', 'role', 'email', 'is_active','department', 'pu_reg_no')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'email')

# Inline for Daily Report
class DailyReportInline(admin.TabularInline):
    model = DailyReport
    extra = 0
    fields = ['date', 'time_in', 'time_out','total_hours', 'task_done', 'problem_faced']
    can_delete = True  # Allow deletion of individual reports

# Inline for Intern Daily Activity
class InternDailyActivityInline(admin.TabularInline):
    model = InternDailyActivity
    extra = 0
    fields = ['date', 'start_time', 'end_time', 'total_hours', 'activity', 'remarks', 'other_remarks']
    can_delete = True  # Allow deletion of individual activities

# Inline for Intern Next Day Planning
class InternNextDayPlanningInline(admin.TabularInline):
    model = InternNextDayPlanning
    extra = 0
    fields = ['date', 'coordination', 'start_time', 'end_time', 'total_hours', 'to_do']
    can_delete = True  # Allow deletion of individual planning records

# Inline for Supervisor Daily Activity
class SupervisorDailyActivityInline(admin.TabularInline):
    model = SupervisorDailyActivity
    extra = 0
    fields = ['date', 'start_time', 'end_time', 'total_hours', 'activity', 'remarks', 'other_remarks']
    can_delete = True  # Allow deletion of individual supervisor activities

# Inline for Supervisor Next Day Planning
class SupervisorNextDayPlanningInline(admin.TabularInline):
    model = SupervisorNextDayPlanning
    extra = 0
    fields = ['date', 'coordination', 'start_time', 'end_time', 'total_hours', 'to_do']
    can_delete = True  # Allow deletion of individual supervisor planning records

# Inline for Project Management Form
class ProjectManagementFormInline(admin.TabularInline):
    model = ProjectManagementForm
    extra = 0
    fields = ['project_name', 'project_manager', 'team_member', 'start_date', 'end_date', 'current_status', 
              'progress', 'priority_level', 'milestone_achievement', 'next_milestone', 'risk_and_challenges', 
              'client_or_stakeholder', 'tools_and_technology', 'custom_tool']
    fk_name = 'project_manager'  # Optional: display as ID inputs instead of dropdowns
    can_delete = True  # Allow deletion of individual project management forms

# Admin for InternProfile
class InternProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'supervisor', 'department', 'first_name', 'last_name', 'phone_no', 'email')
    list_filter = ('department',)
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_no', 'email', 'supervisor__username', 'department__name')
    inlines = [DailyReportInline, InternDailyActivityInline, InternNextDayPlanningInline]

# Admin for SupervisorProfile
class SupervisorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_no')
    search_fields = ('user__username', 'phone_no')
    inlines = [ProjectManagementFormInline, SupervisorDailyActivityInline, SupervisorNextDayPlanningInline]

# Admin for Department Model
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head')
    search_fields = ('name', 'head__username')
    list_filter = ('head',)

class StudentAcademicDetailsInline(admin.TabularInline):
    model=StudentAcademicDetails
    extra=0
    fields= ('degree','started_date','division_gpa','college_university')
    can_delete=True

class PermanentAddressInline(admin.TabularInline):
    model=PermanentAddress
    extra=0
    fields=('provience','district','mc_rm','ward_no')
    can_delete=True

class CurrentAddressInline(admin.TabularInline):
    model=CurrentAddress
    extra=0
    fields=('provience','district','mc_rm','ward_no')
    can_delete=True

class IntrestedCoursesInline(admin.TabularInline):
    model=IntrestedCourses
    extra=0
    fields=('intrested_courses','suitable_time')
    can_delete=True

class StudentsAdmin(admin.ModelAdmin):
    list_display = ('full_name','img_field','gender','date_of_birth','phone_no','email','parents_info',)
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_no', 'email', 'supervisor__username', 'department__name')
    inlines = [StudentAcademicDetailsInline,PermanentAddressInline,CurrentAddressInline,IntrestedCoursesInline]







# Register the models with their respective admin classes
admin.site.register(User, UserAdmin)
admin.site.register(InternProfile, InternProfileAdmin)
admin.site.register(SupervisorProfile, SupervisorProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Students,StudentsAdmin)
