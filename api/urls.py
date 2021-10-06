from django.urls import path

from . import views

import courses.views

urlpatterns = [
    path('sjtu/canteen/<int:id>', views.canteen_detail, name='canteen_detail'),
    path('sjtu/canteen', views.canteen, name='canteen'),
    path('sjtu/library', views.library, name='library'),
    path('sjtu/bathroom', views.bathroom, name='bathroom'),
    path('sjtu/washing_machine/<str:machine_id>', views.washing_machine, name='washing_machine'),
    path('course/lesson', views.lesson, name='lesson'),
    path('course/lesson_info', courses.views.lessons_info, name='lessons_info'),
    path('user/profile', views.user_profile, name='user_profile'),
    path('user/info', views.user_info, name='user_info'),
]
