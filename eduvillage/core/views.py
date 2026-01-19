from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

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
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

# Logout
class UserLogoutView(LogoutView):
    next_page = 'home'
