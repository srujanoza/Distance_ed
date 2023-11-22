from datetime import datetime

from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Course, Student, Order
from .forms import OrderForm, InterestForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
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

            if interested == 1:
                course.interested += 1
                course.save()

                user = request.user
                try:
                    student = Student.objects.get(username=user.username)
                    student.interested_courses.add(course)
                except Student.DoesNotExist:
                    pass  # User is not a student or not found

                return redirect('index')  # Redirect to the main index page

    return render(request, 'myapp/course_detail.html', {'course': course, 'form': form})

# Create your views here.
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            print(user.is_active)

            if user:
                if user.is_active:
                    login(request, user)

                    # Generate the date and time of the current login
                    current_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Store this value as a session parameter (last_login_info)
                    request.session["last_login_info"] = current_login_time

                    # # Set the session expiry to 5 minutes
                    # request.session.set_expiry(300)

                    return HttpResponseRedirect(reverse("index"))
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                return HttpResponse("Invalid login details.")
        else:
            # Don't reinitialize the form here
            pass
    else:
        form = LoginForm()

    return render(request, "myapp/login.html", {"form": form})


@login_required
def user_logout(request):
    # Log out the current user by deleting the request session
    del request.session["last_login_info"]

    # Since SESSION_EXPIRE_AT_BROWSER_CLOSE is True, we don't need to set session expiry here.
    # # Make the user’s session cookies expire when the user’s web browser is closed
    # request.session.set_expiry(0)

    logout(request)

    return HttpResponseRedirect(reverse("login"))


@login_required
def myaccount(request):
    user = request.user
    try:
        student = Student.objects.get(username=user.username)
        # Fetch courses ordered and interested by the student
        courses_ordered = Order.objects.filter(student=student)
        courses_interested = Course.objects.filter(interested_students=student)
        return render(request, "myapp/myaccount.html", {
            "full_name": f"{student.first_name} {student.last_name}",
            "courses_ordered": courses_ordered,
            "courses_interested": courses_interested,
        })
    except Student.DoesNotExist:
        # User is not a student
        return HttpResponse("You are not a registered student!")