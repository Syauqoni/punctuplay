from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('', views.home, name="blog_home"),
    path('home/', views.home),
    path('leaderboard/', views.leaderboard),
    path('logout/', views.logout_user, name='logout'),
]