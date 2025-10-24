from django.urls import path

from . import views

urlpatterns = {
    path('login/', views.login),
    path('register/', views.register),
    path('login/home', views.home),
    path('login/home/leaderboard', views.leaderboard),
    
}