from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Tambahan data user
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    max_xp = models.IntegerField(default=100)   # batas xp per level
    score = models.IntegerField(default=0)
    rank_name = models.CharField(max_length=100, default="Pemula")

    def add_xp(self, amount):
        self.xp += amount

        # naik level jika XP penuh
        while self.xp >= self.max_xp:
            self.xp -= self.max_xp
            self.level += 1
            self.max_xp += 25  # contoh jika difficulty naik tiap level

        self.save()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, "userprofile"):
        instance.userprofile.save()