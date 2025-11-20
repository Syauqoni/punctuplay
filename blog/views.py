from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile   # ← import profil
from django.contrib.auth import logout
from django.shortcuts import redirect


# Create your views here.


def home(request):
    profile = UserProfile.objects.get(user=request.user)

    xp_percent = int((profile.xp / profile.max_xp) * 100)

    context = {
        "profile": profile,
        "xp_percent": xp_percent,
    }
    return render(request, "blog/home.html", context)

def leaderboard(request):
    return render(request, 'blog/leaderboard.html')

def logout_user(request):
    logout(request)
    return redirect('index')

def leaderboard(request):
    # Ambil semua user diurutkan berdasarkan skor tertinggi
    players = UserProfile.objects.order_by('-score')

    return render(request, "blog/leaderboard.html", {"players": players})
