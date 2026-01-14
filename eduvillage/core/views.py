from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to EduVillage – Learning for Every Village")
