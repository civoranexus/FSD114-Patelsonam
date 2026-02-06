from django.contrib import admin
from .models import Course
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course', 'status')
    list_filter = ('status', 'course')
    search_fields = ('name', 'email')

admin.site.register(Course)
