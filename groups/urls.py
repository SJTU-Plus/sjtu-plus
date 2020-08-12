from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('json/<int:root>', views.json, name='json'),
]