from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect
from .forms import EditProfileForm
from .models import Enrollment
from .forms import ProfileForm
from .models import UserProfile

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})


# Home page
def home(request):
    return render(request, 'core/home.html')

# About page
def about(request):
    return render(request, 'core/about.html')

# Dashboard page (login required)
@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')



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

from .forms import ProfileForm

@login_required
def profile(request):
    return render(request, 'core/profile.html')

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'core/my_courses.html', {'enrollments': enrollments})