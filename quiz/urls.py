from django.urls import path, include

from . import views

urlpatterns = {
    path('BenarSalah/', views.BenarSalah),
    path('DragandDrop/', views.DragandDrop, name='dragandDrop'),
    path('Isian/', views.Isian),
    path('MenuKuis/', views.MenuKuis),
    path('Pilgan/', views.Pilgan),
    path('HasilJawaban/', views.HasilJawaban),
    path('blog/', include('blog.urls')),
}