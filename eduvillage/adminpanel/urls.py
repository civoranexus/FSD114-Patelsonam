from django.urls import path
from . import views 
from .views import admin_dashboard, manage_students, add_student,edit_student, delete_student,admin_instructors,admin_courses,admin_reports

urlpatterns = [
    path('dashboard_admin/', admin_dashboard, name='dashboard_admin'),
    path('instructors/', views.admin_instructors, name='admin_instructors'),
    path('courses/', views.admin_courses, name='admin_courses'),
    path('reports/', views.admin_reports, name='admin_reports'),

     # STUDENTS
    path('students/', views.manage_students, name='admin_students'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/delete/<int:index>/', views.delete_student, name='delete_student'),
    path('students/edit/<int:index>/', views.edit_student, name='edit_student'),
    path('students/status/<int:index>/', views.toggle_status, name='toggle_status'),
]
