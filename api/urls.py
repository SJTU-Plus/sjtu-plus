from django.urls import path

from . import views

urlpatterns = [
    path('sjtu/canteen', views.canteen, name='canteen'),
    path('sjtu/library', views.library, name='library'),
]
