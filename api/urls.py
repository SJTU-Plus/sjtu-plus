from django.urls import path

from . import views

urlpatterns = [
    path('sjtu/canteen/<int:id>', views.canteen_detail, name='canteen_detail'),
    path('sjtu/canteen', views.canteen, name='canteen'),
    path('sjtu/library', views.library, name='library'),
    path('course/lesson', views.lesson, name='lesson'),
]
