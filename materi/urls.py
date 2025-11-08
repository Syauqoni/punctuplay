from django.urls import path
from . import views

urlpatterns = [
    path('MateriMenuBelajar/', views.MateriMenuBelajar, name='materi_menu'),
    path('MateriDetail/<int:id>/', views.MateriDetail, name='materi_detail'),
]
