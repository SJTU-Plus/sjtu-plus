from django.urls import path

from . import views

urlpatterns = [
    path('<int:root>', views.index, name='index'),
]
