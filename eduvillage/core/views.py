from asyncio import events
from urllib import request
from django.shortcuts import render, redirect,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse
from .forms import UserForm, EditProfileForm, RegisterForm
from .models import UserProfile, Course, Assignment, Event, Enrollment
import json
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

        'enrollments': enrollments,
        'study_tasks': study_tasks,
        'today_tasks': today_tasks,
    }

    return render(request, 'core/dashboard_student.html', context)


@login_required
def dashboard_instructor(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Allow only instructors
    if profile.role != 'instructor':
        return redirect('login')

    # -------- COURSES & STUDENTS --------
    courses_qs = Course.objects.filter(created_by=request.user)

    if courses_qs.exists():
        total_courses = courses_qs.count()
        total_students = Enrollment.objects.filter(course__in=courses_qs).count()

        courses_list = []
        for course in courses_qs:
            courses_list.append({
                "name": course.name,
                "student_count": Enrollment.objects.filter(course=course).count()
            })

    else:
        # Fake fallback
        total_courses = 3
        total_students = 100

        courses_list = [
            {"name": "Python Programming", "student_count": 32},
            {"name": "AI & ML", "student_count": 28},
            {"name": "Web Development", "student_count": 40},
        ]

    # -------- ASSIGNMENTS --------
    pending_assignments = 5

    # -------- CALENDAR EVENTS --------
    calendar_events = [
        {"title": "Python Class", "start_date": "2026-02-05", "end_date": "2026-02-05", "url": "#"},
        {"title": "AI Assignment Due", "start_date": "2026-02-08", "end_date": "2026-02-08", "url": "#"},
        {"title": "Web Dev Class", "start_date": "2026-02-10", "end_date": "2026-02-10", "url": "#"},
        {"title": "Python Quiz", "start_date": "2026-02-12", "end_date": "2026-02-12", "url": "#"},
    ]

    # -------- NOTIFICATIONS --------
    notifications = [
        "New student enrolled in Python",
        "AI & ML assignment submitted",
        "Web Dev class scheduled tomorrow",
    ]

    # Add upcoming events as notifications
    today = date.today()
    next_week = today + timedelta(days=7)

    for e in calendar_events:
        event_date = date.fromisoformat(e["start_date"])
        if today <= event_date <= next_week:
            notifications.append(
                f"{e['title']} on {event_date.strftime('%d %b %Y')}"
            )

    notifications_count = len(notifications)

    context = {
        "profile": profile,
        "user": request.user,
        "total_courses": total_courses,
        "total_students": total_students,
        "pending_assignments": pending_assignments,
        "notifications_count": notifications_count,
        "notifications": notifications,
        "events": calendar_events,
        "courses_list": courses_list,
    }

    return render(request, "core/dashboard_instructor.html", context)

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
        profile =  UserProfile.objects.get(user=self.request.user)

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
def instructor_my_courses(request):

    courses = [
        {"name": "Cybersecurity Essentials", "subject": "Cybersecurity", "student_count": 25},
        {"name": "Data Science 101", "subject": "Data Science", "student_count": 30},
        {"name": "Machine Learning A-Z", "subject": "Machine Learning", "student_count": 28},
    ]

    return render(
        request,
        "core/instructor_my_courses.html",
        {"courses": courses}
    )


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
def contact(request):
    return render(request, 'core/contact.html')

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    already_enrolled = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists()

    return render(request, 'core/course_detail.html', {
        'course': course,
        'already_enrolled': already_enrolled
    })


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

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

@login_required
def grades(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

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

def dashboard(request):
    return render(request, 'dashboard.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta


@login_required
def instructor_calendar(request):
    # Month navigation
    year = int(request.GET.get("year", date.today().year))
    month = int(request.GET.get("month", date.today().month))

    first_day = date(year, month, 1)
    start_day = first_day - timedelta(days=first_day.weekday())
    today = date.today()

    # 🔹 CENTRAL EVENT STORE (FAKE DATA – READY FOR DB)
    calendar_events = [
        {"title": "AI Class", "date": date(year, month, 3), "type": "class"},
        {"title": "DBMS Class", "date": date(year, month, 5), "type": "class"},
        {"title": "ML Assignment Due", "date": date(year, month, 10), "type": "assignment"},
        {"title": "AI Unit Test", "date": date(year, month, 15), "type": "exam"},
        {"title": "DBMS Mid Exam", "date": date(year, month, 20), "type": "exam"},
        {"title": "ML Assignment Review", "date": date(year, month, 25), "type": "assignment"},
    ]

    # Build calendar days
    days = []
    for i in range(42):  # 6 weeks view
        current = start_day + timedelta(days=i)

        calendar_events= [
            e for e in calendar_events if e["date"] == current
        ]

        days.append({
            "date": current,
            "events": calendar_events,
            "is_today": current == today,
            "in_month": current.month == month
        })
    # Split into weeks (6 lists of 7 days each)
    weeks = [days[i:i + 7] for i in range(0, 42, 7)]

    context = {
        "weeks": weeks,
        "month_year": first_day.strftime("%B %Y"),
        "prev_month": (first_day - timedelta(days=1)),
        "next_month": (first_day + timedelta(days=32)).replace(day=1),
    }

    return render(request, "core/calendar.html", context)


@login_required
def notifications(request):

    notifications = [
        "New student enrolled in Python",
        "AI Assignment submitted",
        "Web Dev class scheduled tomorrow",
        "Python Quiz on 12 Feb",
        "Project presentation on 18 Feb",
    ]

    return render(request, "core/notifications.html", {
        "notifications": notifications
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Enrollment, UserProfile

@login_required
def student_attendance(request):

    courses = [
        "Cybersecurity Essentials",
        "Data Science 101",
        "Machine Learning A-Z",
    ]

    students = [
        {"name": "Aarav Patel", "roll": "CS01"},
        {"name": "Neha Sharma", "roll": "CS02"},
        {"name": "Rahul Verma", "roll": "CS03"},
        {"name": "Priya Singh", "roll": "CS04"},
    ]

    return render(
        request,
        "core/student_attendance.html",
        {
            "courses": courses,
            "students": students,
        }
    )



@login_required
def student_my_courses(request):
    # Get user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Allow only students
    if profile.role != 'student':
        return redirect('login')

    # Get enrolled courses for student
    enrollments = Enrollment.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'enrollments': enrollments,
    }

    return render(request, 'core/my_courses.html', context)
from django.contrib.auth.decorators import login_required

@login_required
def my_courses(request):
    courses = Course.objects.filter(
        enrollment__student=request.user
    )
    return render(request, 'core/my_courses.html', {
        'courses': courses
    })
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    already_enrolled = Enrollment.objects.filter(
        user=request.user,
        course=course
    ).exists()

    return render(request, 'core/course_detail.html', {
        'course': course,
        'already_enrolled': already_enrolled
    })
def courses(request):
    courses = Course.objects.all()

    enrolled_courses = []
    if request.user.is_authenticated:
        enrolled_courses = Course.objects.filter(
            enrollment__user=request.user
        )

    return render(request, 'core/courses.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses
    })
