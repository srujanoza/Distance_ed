from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Course, Student
from .forms import OrderForm, InterestForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


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


def courses(request):
    course_list = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'course_list': course_list})


def place_order(request):
    msg = ''
    course_list = Course.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            # Check if the course price is greater than $4000.00 and apply discount
            if order.course.price > 4000.00:
                order.discount()

            # Check if the student ordered a number of levels that exceeds the course's levels
            if order.levels > course_list.get(id=order.course.id).get_level_id():
                msg = 'You exceeded the number of levels for this course.'
            else:
                msg = 'Your course has been ordered successfully.'
                order.order_status = 0
            order.save()
        else:
            msg = 'Form is not valid.'
    else:
        form = OrderForm()

    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'course_list': course_list})


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    form = InterestForm()

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interested = form.cleaned_data['interested']

            # If interested is 1, increment the interested field for the course
            if interested == 1:
                course.interested += 1
                course.save()
                return redirect('index')  # Redirect to the main index page

    return render(request, 'myapp/course_detail.html', {'course': course, 'form': form})


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'myapp/login.html', {'message': 'your account is disabled'})
        else:
            return render(request, 'myapp/login.html', {'message': 'Invalid login details'})
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def myaccount(request):
    user = request.user
    student = Student.objects.filter(first_name__iexact=user)
    print(student)
    # Check if the logged-in user is a Student
    if student.status == 'GD':

        # Get the first and last name of the student
        first_name = user.first_name
        last_name = user.last_name

        # Get all courses ordered by the student
        ordered_courses = Course.objects.filter(order__student=user)

        # Get all courses the student is interested in
        interested_courses = user.interested_courses.all()

        context = {
            'first_name': first_name,
            'last_name': last_name,
            'ordered_courses': ordered_courses,
            'interested_courses': interested_courses,
        }

        return render(request, 'myapp/myaccount.html', context)
    else:
        return render(request, 'myapp/myaccount.html', {'message': 'You are not a registered Student!'})
