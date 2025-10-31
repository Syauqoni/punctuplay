from django.urls import path, include

from . import views

urlpatterns = {
    path('MateriDetail/', views.MateriDetail),
    path('MateriMenuBelajar/', views.MateriMenuBelajar),
}