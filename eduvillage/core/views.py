from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to EduVillage – Learning for Every Village")
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')
# Home page view
def home(request):
    return render(request, 'core/home.html')
