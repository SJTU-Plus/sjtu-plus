from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate, name='generate'),
    path('verify', views.verify, name='verify'),
]
