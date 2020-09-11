from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verify/', views.verify, name='verify'),
    path('freshmen-groups/', lambda _: redirect('/categories/freshmen-groups')),
    path('subjects/', lambda _: redirect('/categories/subjects')),
    path('websites/', lambda _: redirect('/categories/websites'))
]
