from django.db import models

class Materi(models.Model):
    judul = models.CharField(max_length=200)
    teks = models.TextField()
    gambar = models.ImageField(upload_to='materi_images/', blank=True, null=True)

    def __str__(self):
        return self.judul
