from django.db import models
from django.contrib.auth.models import User
from accounts.models import UserProfile   # PENTING agar tidak bentrok


class Quiz(models.Model):
    judul = models.CharField(max_length=200)
    gambar = models.CharField(max_length=300, blank=True, null=True)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.judul


class Soal(models.Model):
    TIPE_SOAL = [
        ("pilgan", "Pilihan Ganda"),
        ("dragdrop", "Drag & Drop"),
        ("isian", "Isian"),
        ("benarsalah", "Benar atau Salah"),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="soal")
    tipe = models.CharField(max_length=20, choices=TIPE_SOAL)
    urutan = models.IntegerField(default=1)
    pertanyaan = models.TextField()

    # Pilgan
    opsi_a = models.CharField(max_length=255, blank=True, null=True)
    opsi_b = models.CharField(max_length=255, blank=True, null=True)
    opsi_c = models.CharField(max_length=255, blank=True, null=True)
    opsi_d = models.CharField(max_length=255, blank=True, null=True)

    # Drag & Drop
    jawaban_drag = models.JSONField(blank=True, null=True)

    # Isian
    jawaban_isian = models.JSONField(blank=True, null=True)

    # Benar / Salah
    jawaban_benarsalah = models.BooleanField(blank=True, null=True)

    # Kunci jawaban umum
    jawaban_benar = models.CharField(max_length=255, blank=True, null=True)

    # Tambahan penting
    poin = models.IntegerField(default=10)  # poin untuk leaderboard
    penjelasan = models.TextField(blank=True, null=True)  # alasan jawaban benar

    def __str__(self):
        return f"{self.urutan}. {self.pertanyaan[:40]}"


class UserJawaban(models.Model):
    """Simpan jawaban user untuk setiap soal"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    soal = models.ForeignKey(Soal, on_delete=models.CASCADE)
    jawaban_user = models.TextField()

    benar = models.BooleanField(default=False)
    xp_didapat = models.IntegerField(default=0)
    poin_didapat = models.IntegerField(default=0)

    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Soal {self.soal.id}"


class ProgressQuiz(models.Model):
    """Progress user dalam 1 kuis"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    total_benar = models.IntegerField(default=0)
    total_salah = models.IntegerField(default=0)
    xp_total = models.IntegerField(default=0)
    selesai = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.judul}"


class Lencana(models.Model):
    """Lencana sesuai total XP atau pencapaian"""
    nama = models.CharField(max_length=100)
    deskripsi = models.TextField(blank=True, null=True)
    xp_minimal = models.IntegerField(default=0)

    def __str__(self):
        return self.nama
    
class RiwayatKuis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    skor = models.IntegerField(default=0)   # ← UBAH NAMA FIELD AGAR SESUAI
    terakhir_main = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'quiz')

    def __str__(self):
        return f"{self.user.username} - {self.quiz.judul} - {self.skor}"

