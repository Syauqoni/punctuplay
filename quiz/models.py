from django.db import models

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

    # Tipe soal
    tipe = models.CharField(max_length=20, choices=TIPE_SOAL)

    # Urutan soal (biar kamu bisa atur sendiri urutannya)
    urutan = models.IntegerField(default=1)

    # Pertanyaan utama
    pertanyaan = models.TextField()

    # PILIHAN GANDA
    opsi_a = models.CharField(max_length=255, blank=True, null=True)
    opsi_b = models.CharField(max_length=255, blank=True, null=True)
    opsi_c = models.CharField(max_length=255, blank=True, null=True)
    opsi_d = models.CharField(max_length=255, blank=True, null=True)

    # DRAG & DROP → contoh: [",", ",", ".", "!"]
    jawaban_drag = models.JSONField(blank=True, null=True)

    # ISIAN → contoh: [" , ", " . ", "!"]
    jawaban_isian = models.JSONField(blank=True, null=True)

    # BENAR / SALAH → True / False
    jawaban_benarsalah = models.BooleanField(blank=True, null=True)

    # Untuk pilihan ganda → "A", "B", "C", "D"
    jawaban_benar = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.urutan}. ({self.tipe}) {self.pertanyaan[:40]}"
