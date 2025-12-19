from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import UserProfile
from django.contrib.auth import logout


@login_required(login_url='login')
def home(request):
    profile = UserProfile.objects.get(user=request.user)

    xp_percent = 0
    if profile.max_xp > 0:
        xp_percent = int((profile.xp / profile.max_xp) * 100)

    context = {
        "profile": profile,
        "xp_percent": xp_percent,
    }
    return render(request, "blog/home.html", context)


def leaderboard(request):
    players = UserProfile.objects.order_by('-total_poin', 'total_time_spent')
    return render(request, "blog/leaderboard.html", {"players": players})


def logout_user(request):
    logout(request)
    return redirect('index')
