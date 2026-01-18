from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password'})
    return render(request, 'core/login.html')

# Logout page
def user_logout(request):
    logout(request)
    return redirect('home')
