from django.urls import path

from . import views

app_name = "courses"
urlpatterns = [
    path('api/courses/lessons_info', views.lessons_info, name='lessons_info'),
]
