from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    ...

# Create your views here.
def admin_dashboard(request):
    context = {
        'total_students': 120,
        'total_instructors': 15,
        'total_courses': 25,
        'total_assignments': 80,
    }
    return render(request, 'adminpanel/dashboard_admin.html', context)

def manage_students(request):
    return render(request, 'adminpanel/student_admin.html')

def admin_instructors(request):
    return render(request, 'adminpanel/instructor_admin.html')

def admin_courses(request):
    return render(request, 'adminpanel/course_admin.html')
def admin_reports(request):
    context = {
        'total_students': 120,
        'total_instructors': 15,
        'total_courses': 25,
    }
    return render(request, 'adminpanel/report_admin.html', context)
