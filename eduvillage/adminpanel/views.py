from django.shortcuts import render, redirect
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
    students = request.session.get('students', [])

    total = len(students)
    active = sum(1 for s in students if s['status'] == 'Active')
    inactive = total - active

    return render(request, 'adminpanel/student_admin.html', {
        'students': students,
        'total': total,
        'active': active,
        'inactive': inactive
    })


def add_student(request):
    if request.method == 'POST':
        students = request.session.get('students', [])
        students.append({
            'name': request.POST['name'],
            'email': request.POST['email'],
            'course': request.POST['course'],
            'status': 'Active'
        })
        request.session['students'] = students
    return redirect('admin_students')


def delete_student(request, index):
    students = request.session.get('students', [])
    if index < len(students):
        students.pop(index)
        request.session['students'] = students
    return redirect('admin_students')


def edit_student(request, index):
    students = request.session.get('students', [])
    if request.method == 'POST':
        students[index]['name'] = request.POST['name']
        students[index]['email'] = request.POST['email']
        students[index]['course'] = request.POST['course']
        request.session['students'] = students
        return redirect('admin_students')

    return render(request, 'adminpanel/edit_student.html', {
        'student': students[index],
        'index': index
    })


def toggle_status(request, index):
    students = request.session.get('students', [])
    if students[index]['status'] == 'Active':
        students[index]['status'] = 'Inactive'
    else:
        students[index]['status'] = 'Active'
    request.session['students'] = students
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
