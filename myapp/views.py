from django.shortcuts import get_object_or_404, render
from .models import Category, Course


def index(request):
    category_list = Category.objects.all().order_by('id')[:10]
    course_list = Course.objects.all().order_by('-price')[:5]
    '''View
    response = HttpResponse()
    heading1 = '<h2> List of categories: </h2>'
    response.write(heading1)
    for category in category_list:
        para = '<p>' + str(category.id) + ': ' + '<a href="/myapp/category/' + str(category.id) + '">' + str(category) + '</a>' + '</p>'
        response.write(para)
    heading2 = '<br /><br /><h2> List of courses (sorted by price, descending): </h2>'
    response.write(heading2)
    for course in course_list:
        para = '<p>' + str(course) + ' - Price: $' + str(course.price) + '</p>'
        response.write(para)
    link = f'<br /><br /><a href="/myapp/about/">About Page</a>'
    response.write(link)

    return response
    '''
    return render(request, 'myapp/index0.html', {'category_list': category_list})


def about(request):
    # response = HttpResponse()
    # heading1 = '<h2>About Us</h2>'
    # response.write(heading1)
    # para = '<p>This is a Distance Education Website! Search our Categories to find all available Courses.</p>'
    # response.write(para)
    # link = f'<br /><br /><a href="/myapp/">Go Back Home</a>'
    # response.write(link)
    # return response
    return render(request, 'myapp/about0.html')


def detail(request, category_no):
    category = get_object_or_404(Category, pk=category_no)
    course_list = Course.objects.filter(categories=category)
    '''View
    response = HttpResponse()
    heading1 = '<h2>' + str(category) + '</h2>'
    response.write(heading1)
    for course in course_list:
        para = '<p>' + str(course.title) + '</p>'
        response.write(para)
    link = f'<br /><br /><a href="/myapp/">Go Back Home</a>'
    response.write(link)
    return response
    '''
    return render(request, 'myapp/detail0.html', {'category': category, 'course_list': course_list})
