from django.shortcuts import render

# Create your views here.
def BenarSalah(request):
    return render(request, 'quiz/BenarSalah.html')

def DragandDrop(request):
    return render(request, 'quiz/DragandDrop.html')

def Isian(request):
    return render(request, 'quiz/Isian.html')

def MenuKuis(request):
    return render(request, 'quiz/MenuKuis.html')

def Pilgan(request):
    return render(request, 'quiz/Pilgan.html')