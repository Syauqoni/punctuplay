from django.urls import path, include
from . import views

urlpatterns = [
    path('MenuKuis/', views.MenuKuis, name='MenuKuis'),
    path('<int:quiz_id>/soal/<int:nomor>/', views.tampil_soal, name='tampil_soal'),
    path("simpan-jawaban/", views.simpan_jawaban_ajax, name="simpan_jawaban_ajax"),
    path("ajax/timer/", views.simpan_timer_ajax, name="simpan_timer_ajax"),
    path('HasilJawaban/<int:quiz_id>/', views.HasilJawaban, name='hasil_jawaban'),
    path('blog/', include('blog.urls')),
    path('logout/', views.logout_user, name='logout'),
]
