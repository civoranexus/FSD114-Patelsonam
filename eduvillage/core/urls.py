from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import home, about, dashboard, UserLoginView, signup, UserLogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path(
    'password-change/',
    auth_views.PasswordChangeView.as_view(
        template_name='core/change_password.html',
        success_url='/profile/'
    ),
    name='password_change'
),
   path('register/', views.register, name='register'),
   path('courses/', views.courses, name='courses'),
   path('contact/', views.contact, name='contact'),
   path('my-profile/', views.profile, name='my_profile'),
   path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
   path('student/dashboard/', views.dashboard_student, name='dashboard_student'),  


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
