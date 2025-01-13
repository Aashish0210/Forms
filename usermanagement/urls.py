from django.urls import path
from . import views

urlpatterns = [
    path('', views.default_page, name='default_page'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('intern_home/', views.intern_home, name='intern_home'),
    path('supervisor_home/', views.supervisor_home, name='supervisor_home'),
    path('department_home/', views.department_home, name='department_home'),
    path('superuser_home/', views.superuser_dashboard, name='superuser_dashboard'),  # Superuser dashboard
    path('role_redirect/', views.redirect_to_role_home, name='redirect_to_role_home'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),  # PDF generation
]
