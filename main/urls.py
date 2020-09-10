from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('verify/', views.verify, name='verify'),
    path('freshmen-groups/', lambda _: redirect('/categories/5')),
    path('subjects/', lambda _: redirect('/categories/15')),
    path('websites/', lambda _: redirect('/categories/18'))
]
