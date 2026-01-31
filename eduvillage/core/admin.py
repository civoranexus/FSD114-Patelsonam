from django.contrib import admin
from .models import Village, UserProfile, Course, Enrollment

admin.site.register(Village)
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Enrollment)
