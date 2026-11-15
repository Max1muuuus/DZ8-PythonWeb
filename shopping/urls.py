from django.urls import path
from . import views

urlpatterns = [
    path('', views.shopping_list, name='shopping_list'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
]
