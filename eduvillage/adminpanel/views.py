from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student

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
    students = Student.objects.all()

    context = {
        'students': students,
        'total_students': students.count(),
        'active_students': students.filter(status='Active').count(),
        'inactive_students': students.filter(status='Inactive').count(),
    }
    return render(request, 'adminpanel/student_admin.html', context)
def student_list(request):
    students = Student.objects.all()

    total_students = students.count()
    active_students = students.filter(status='Active').count()
    inactive_students = students.filter(status='Inactive').count()
def add_student(request):
    if request.method == 'POST':
        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            course=request.POST['course'],
            status=request.POST['status']
        )
        return redirect('admin_students')

    return render(request, 'adminpanel/add_student.html')
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.email = request.POST['email']
        student.course = request.POST['course']
        student.status = request.POST['status']
        student.save()
        return redirect('admin_students')

    return render(request, 'adminpanel/edit_student.html', {'student': student})
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('admin_students')

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
