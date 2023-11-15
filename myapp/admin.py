from django.contrib import admin
from .models import Category, Course, Instructor, Order, Student

# Register your models here.
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Order)
admin.site.register(Student)
