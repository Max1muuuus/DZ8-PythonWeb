from django.urls import path

from . import views

app_name = 'personal_cabinet'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('tasks/', views.tasks, name='tasks'),
    path('settings/', views.settings, name='settings'),
]
