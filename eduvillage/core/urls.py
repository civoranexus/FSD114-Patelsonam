from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
