from django.urls import path
from . import views 
from .views import admin_dashboard, manage_students, add_student,edit_student, delete_student,admin_instructors,admin_courses,admin_reports

urlpatterns = [
    path('dashboard_admin/', admin_dashboard, name='dashboard_admin'),
    path('instructors/', views.admin_instructors, name='admin_instructors'),
    path('courses/', views.admin_courses, name='admin_courses'),
    path('reports/', views.admin_reports, name='admin_reports'),

     # STUDENTS
    path('dashboard_admin/', admin_dashboard, name='dashboard_admin'),
    path('students/', manage_students, name='admin_students'),
    path('instructors/', views.admin_instructors, name='admin_instructors'),
    path('courses/', views.admin_courses, name='admin_courses'),
    path('reports/', views.admin_reports, name='admin_reports'),
    ]