from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Sistem XP & Level
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    max_xp = models.IntegerField(default=300)   # XP penuh sebelum naik level

    # Sistem poin untuk leaderboard
    total_poin = models.IntegerField(default=0)

    # Rank / lencana teks
    rank_name = models.CharField(max_length=100, default="Pemula tanda baca")
    total_time_spent = models.FloatField(default=0)
    total_xp = models.IntegerField(default=0)


 


    def add_xp(self, amount):
        """Tambah XP sekaligus cek naik level, max level 15000"""
        if self.level >= 15000:
            return
        
        self.total_xp += amount
        self.xp += amount

        while self.xp >= self.max_xp and self.level < 15000:
            self.level += 1
            self.max_xp += 300
            if self.max_xp > 15000:
                self.max_xp = 15000  

        self.save()

    def update_rank(self):
        if self.level < 2:
            self.rank_name = "Pemula tanda baca"
        elif self.level < 3:
            self.rank_name = "Penjelajah kalimat"
        elif self.level < 4:
            self.rank_name = "Ahli tanda baca dasar"
        elif self.level < 5:
            self.rank_name = "Master-nya Tanda Baca"
        else:
            self.rank_name = "Grandmaster Punctuplay"
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
