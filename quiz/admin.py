from django.contrib import admin
from .models import Quiz, Soal, RiwayatKuis  

class SoalInline(admin.TabularInline):
    model = Soal
    extra = 1  # jumlah form kosong yang muncul
    fields = (
        'tipe',
        'pertanyaan',
        'opsi_a', 'opsi_b', 'opsi_c', 'opsi_d',
        'jawaban_drag',
        'jawaban_isian',
        'jawaban_benarsalah',
        'jawaban_benar',
    )

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('judul', 'level')
    inlines = [SoalInline]

@admin.register(Soal)
class SoalAdmin(admin.ModelAdmin):
    list_display = ('pertanyaan','urutan', 'tipe', 'quiz')

@admin.register(RiwayatKuis)
class RiwayatKuisAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'skor')