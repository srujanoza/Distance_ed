from django.shortcuts import get_object_or_404, render
from .models import Category, Course, Instructor, Student


def index(request):
    category_list = Category.objects.all().order_by('id')[:10]
    course_list = Course.objects.all().order_by('-price')[:5]
    context = {
        'category_list': category_list,
        'course_list': course_list,
    }
    return render(request, 'myappF23/index.html', context)


def about(request):
    return render(request, 'myappF23/about.html')


def detail(request, category_no):
    category = get_object_or_404(Category, pk=category_no)
    course_list = Course.objects.filter(categories=category)
    return render(request, 'myappF23/details.html', {'category': category, 'course_list': course_list})

