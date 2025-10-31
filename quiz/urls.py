from django.urls import path, include

from . import views

urlpatterns = {
    path('BenarSalah/', views.BenarSalah),
    path('DragandDrop/', views.DragandDrop),
    path('Isian/', views.Isian),
    path('MenuKuis/', views.MenuKuis),
    path('Pilgan/', views.Pilgan),
}