from django.contrib import admin
from .models import Category, Course, Instructor, Student

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Student)
