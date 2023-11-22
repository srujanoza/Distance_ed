from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    # path("", RedirectView.as_view(url=reverse_lazy('user_login')), name="redirect_to_login"),
    # path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("myaccount/", views.myaccount, name="myaccount"),
    path('about/', views.about, name='about'),
    path('category/<int:category_no>/', views.detail, name='detail'),
    path('courses/', views.courses, name='courses'),
    path('place_order/', views.place_order, name='place_order'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('index/', views.index, name='index'),
    path('', views.user_login, name='user_login'),
]