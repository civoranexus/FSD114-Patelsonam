from django.shortcuts import render, redirect,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from .forms import UserForm, EditProfileForm, RegisterForm
from .models import UserProfile, Course, Enrollment,Grade
from datetime import date, timedelta
from .models import StudyTask

# Edit profile
@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = EditProfileForm(instance=profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'core/edit_profile.html', context)


# Home page
def home(request):
    return render(request, 'core/home.html')


# About page
def about(request):
    return render(request, 'core/about.html')


# Role-based dashboard
@login_required
def dashboard(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if profile.role == 'student':
        template_name = 'core/dashboard_student.html'
    elif profile.role == 'instructor':
        template_name = 'core/dashboard_instructor.html'
    else:
        template_name = 'core/dashboard_admin.html'

    context = {'profile': profile, 'user': request.user}
    return render(request, template_name, context)
@login_required
def dashboard_student(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Allow only students
    if profile.role != 'student':
        return redirect('login')

    # Enrolled courses
    enrollments = Enrollment.objects.filter(user=request.user)

    # Dummy Alerts
    notices = [
        {'type': 'Notice', 'message': 'Campus will be closed on 2026-02-05'},
        {'type': 'Fee', 'message': 'Tuition fee due on 2026-02-10'},
    ]

    # Dummy Grade
    grades = [
        {
            'course': 'Computer Science',
            'score': 88,
            'grade': 'A'
        }
    ]
    study_tasks = StudyTask.objects.filter(
        user=request.user
    ).order_by('study_date')[:5]

    today_tasks = StudyTask.objects.filter(
        user=request.user,
        study_date=date.today()
    )

    context = {
        'profile': profile,
        'notices': notices,
        'grades': grades,
        'enrollments': enrollments,
        'study_tasks': study_tasks,
        'today_tasks': today_tasks,
    }

    return render(request, 'core/dashboard_student.html', context)

# Instructor dashboard
@login_required
def dashboard_instructor(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if profile.role != 'instructor':
        return redirect('login')

    courses = Course.objects.filter(created_by=request.user)
    total_courses = courses.count()
    total_students = Enrollment.objects.filter(course__in=courses).count()

    context = {'profile': profile, 'total_courses': total_courses, 'total_students': total_students}
    return render(request, 'core/dashboard_instructor.html', context)


# Admin dashboard
@login_required
def dashboard_admin(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Allow only admin
    if profile.role != 'admin':
        return redirect('login')
    
    # Admin can see total users, courses, etc.
    from django.contrib.auth.models import User
    total_users = User.objects.count()
    total_courses = Course.objects.count()
    
    context = {
        'profile': profile,
        'total_users': total_users,
        'total_courses': total_courses,
    }
    
    return render(request, 'core/dashboard_admin.html', context)

# Login page
class UserLoginView(LoginView):
    template_name = 'core/login.html'

    def get_success_url(self):
        profile = UserProfile.objects.get(user=self.request.user)

        if profile.role == 'student':
            return reverse('dashboard_student')
        elif profile.role == 'instructor':
            return reverse('dashboard_instructor')
        elif profile.role == 'admin':
            return reverse('dashboard_admin')

        return reverse('home')


# Signup page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


# Logout
class UserLogoutView(LogoutView):
    next_page = 'home'


# Profile page
@login_required
def profile(request):
    return render(request, 'core/profile.html')


# My courses page
@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')

    return render(request, 'core/my_courses.html', {
        'enrollments': enrollments
    })

# Register new user
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


# Courses page
def courses(request):
    return render(request, 'core/courses.html')


# Contact page
def contact(request):
    return render(request, 'core/contact.html')


# Enroll in course
@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    return redirect('my_courses')


# Study planner
@login_required
def study_planner(request):
    today = date.today()
    week = [today + timedelta(days=i) for i in range(7)]

    planner = []
    task_counter = 1  # unique ID for each task
    for day in week:
        tasks = [
            {'id': task_counter, 'subject': 'Math', 'duration': 1},
            {'id': task_counter + 1, 'subject': 'English', 'duration': 2},
            {'id': task_counter + 2, 'subject': 'Science', 'duration': 1.5},
        ]
        planner.append({
            'date': day,
            'tasks': tasks
        })
        task_counter += 3

    return render(request, 'core/study_planner.html', {'planner': planner})
# Assignments page
@login_required
def assignments(request):
    dummy_assignments = [
        {'title': 'Math Homework', 'due_date': '2026-02-01'},
        {'title': 'Science Project', 'due_date': '2026-02-05'},
        {'title': 'English Essay', 'due_date': '2026-02-10'},
    ]
    context = {'title': 'Assignments', 'assignments': dummy_assignments}
    return render(request, 'core/assignments.html', context)


# Grades page
@login_required
def grades(request):
    return render(request, 'core/grades.html')


# Attendance page
@login_required
def attendance(request):
    return render(request, 'core/attendance.html')


# AI Tutor page
@login_required
def ai_tutor(request):
    return render(request, 'core/ai_tutor.html')

@login_required
def grades(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if profile.role != 'student':
        return redirect('login')

    grades = Grade.objects.filter(student=request.user)

    context = {
        'grades': grades
    }

    return render(request, 'core/grades.html', context)
def student_attendance(request):
    return render(request,'student/attendance.html')

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)

    if request.method == 'POST':
        task.subject = request.POST.get('subject')
        task.topic = request.POST.get('topic')
        task.study_date = request.POST.get('study_date')
        task.duration_hours = request.POST.get('duration')
        task.save()
        return redirect('study_planner')

    return render(request, 'edit_task.html', {'task': task})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(StudyTask, id=task_id, user=request.user)
    task.delete()
    return redirect('study_planner')
@login_required
def weekly_planner(request):
    today = date.today()
    week_end = today + timedelta(days=6)

    tasks = StudyTask.objects.filter(
        user=request.user,
        study_date__range=[today, week_end]
    ).order_by('study_date')

    return render(request, 'core/weekly_planner.html', {'tasks': tasks})



