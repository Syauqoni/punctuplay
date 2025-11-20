from django.shortcuts import render
from .models import Quiz
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.
def BenarSalah(request):
    return render(request, 'quiz/BenarSalah.html')

def DragandDrop(request):
    return render(request, 'quiz/DragandDrop.html')

def Isian(request):
    return render(request, 'quiz/Isian.html')

def Pilgan(request):
    return render(request, 'quiz/Pilgan.html')

def HasilJawaban(request):
    return render(request, 'quiz/HasilJawaban.html')

def MenuKuis(request):
    level = request.GET.get("level", "1")

    kuis_list = Quiz.objects.filter(level=level)

    return render(request, "quiz/MenuKuis.html", {
        "kuis_list": kuis_list,
        "level": level,   
    })

def logout_user(request):
    logout(request)
    return redirect('index')