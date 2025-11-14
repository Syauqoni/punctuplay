from django.shortcuts import render
from .models import Quiz

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
    kuis_list = Quiz.objects.all()
    return render(request, "quiz/MenuKuis.html", {"kuis_list": kuis_list})