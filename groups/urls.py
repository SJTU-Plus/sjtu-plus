from django.urls import path

from . import views

urlpatterns = [
    path('<int:root>', views.index, name='index'),
    path('freshmen-groups', views.index, {"root": 5}, name='index'),
    path('subjects', views.index, {"root": 15}, name='index'),
    path('websites', views.website, {"root": 18}, name='website')
]
