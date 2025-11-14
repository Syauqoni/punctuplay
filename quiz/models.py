from django.db import models

class Quiz(models.Model):
    judul = models.CharField(max_length=200)
    gambar = models.CharField(max_length=300, blank=True, null=True)
    level = models.IntegerField(default=1)

    def __str__(self):
        return self.judul
