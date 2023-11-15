from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<int:category_no>/', views.detail, name='detail'),
    path('courses/', views.courses, name='courses'),
    path('place_order/', views.place_order, name='place_order'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail')
]
