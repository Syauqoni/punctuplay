from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Sistem XP & Level
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    max_xp = models.IntegerField(default=100)   # XP penuh sebelum naik level

    # Sistem poin untuk leaderboard
    total_poin = models.IntegerField(default=0)

    # Rank / lencana teks
    rank_name = models.CharField(max_length=100, default="Pemula")

    def add_xp(self, amount):
        """Tambah XP sekaligus cek naik level"""
        self.xp += amount

        # naik level otomatis
        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp += 25

        self.save()

    def add_poin(self, poin):
        """Tambah poin untuk leaderboard"""
        self.total_poin += poin
        self.save()

    def __str__(self):
        return self.user.username


# Auto create profile saat user dibuat
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()
