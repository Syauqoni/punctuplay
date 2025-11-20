from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from accounts.models import UserProfile   # ← import profil



def login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # sesuai form
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("/blog/home/")  
        else:
            messages.error(request, "Username atau password salah!")

    return render(request, "accounts/login.html")



def register(request):
    if request.method == "POST":
        name = request.POST.get("name")  # sesuai HTML
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        # Validasi
        if password != password_confirmation:
            messages.error(request, "Konfirmasi password tidak cocok!")
            return render(request, "accounts/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan!")
            return render(request, "accounts/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email sudah digunakan!")
            return render(request, "accounts/register.html")

        # Membuat user baru
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name  # simpan nama di first_name
        )

        user.save()

        messages.success(request, "Akun berhasil dibuat! Silakan login.")
        return redirect("/accounts/login/")

    return render(request, "accounts/register.html")

def leaderboard(request):
    # Ambil semua user diurutkan berdasarkan skor tertinggi
    players = UserProfile.objects.order_by('-score')

    return render(request, "leaderboard.html", {"players": players})