from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserForm, EditProfileForm
from .models import UserProfile, Enrollment
from django.shortcuts import redirect, get_object_or_404
from .models import Course, Enrollment
from .forms import RegisterForm

@login_required
def edit_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = EditProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = EditProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'core/edit_profile.html', context)


# Home page
def home(request):
    return render(request, 'core/home.html')

# About page
def about(request):
    return render(request, 'core/about.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def dashboard(request):
    # Get or create profile (safety)
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # Role-based dashboard rendering
    if profile.role == 'student':
        template_name = 'core/dashboard_student.html'
    elif profile.role == 'instructor':
        template_name = 'core/dashboard_instructor.html'
    else:
        template_name = 'core/dashboard_admin.html'

    context = {
        'profile': profile,
        'user': request.user
    }

    return render(request, template_name, context)



# Login page
class UserLoginView(LoginView):
    template_name = 'core/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Logged in successfully!")
        return super().form_valid(form)

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
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'core/my_courses.html', {'enrollments': enrollments})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})
def courses(request):
    return render(request, 'core/courses.html')

def contact(request):
    return render(request, 'core/contact.html')
@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    return redirect('my_courses')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard_student(request):
    return render(request, 'core/dashboard_student.html')