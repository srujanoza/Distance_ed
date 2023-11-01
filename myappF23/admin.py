# Register your models here.

from django.contrib import admin
from django.db import models
from .models import Category, Course, Student, Instructor

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Instructor)