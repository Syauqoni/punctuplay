from django.urls import path, include
from . import views

urlpatterns = [
    path('MenuKuis/', views.MenuKuis, name='MenuKuis'),
    path('<int:quiz_id>/soal/<int:nomor>/', views.tampil_soal, name='tampil_soal'),
    path('HasilJawaban/<int:quiz_id>/', views.HasilJawaban, name='hasil_jawaban'),
    path('blog/', include('blog.urls')),
    path('logout/', views.logout_user, name='logout'),
]
