from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

def home(request):
    return render(request, 'core/home.html')
def about(request):
    return render(request, 'core/about.html')


class UserLoginView(LoginView):
    template_name = 'core/login.html'

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')
