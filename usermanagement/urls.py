from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('Sera_Digital_Hub/', views.default_page, name='default_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('intern_home/', views.intern_home, name='intern_home'),
    path('employee_home/', views.employee_home, name='employee_home'),
    path('supervisor_home/', views.supervisor_home, name='supervisor_home'),
    path('department_home/', views.department_home, name='department_home'),
    path('superuser_home/', views.superuser_dashboard, name='superuser_dashboard'),  # Superuser dashboard
    path('role_redirect/', views.redirect_to_role_home, name='redirect_to_role_home'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),  # PDF generation
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
