from django.shortcuts import render, get_object_or_404
from .models import Materi

def MateriMenuBelajar(request):
    materi_list = Materi.objects.all()
    return render(request, 'materi/MateriMenuBelajar.html', {'materi_list': materi_list})

def MateriDetail(request, id):
    materi = get_object_or_404(Materi, id=id)
    return render(request, 'materi/MateriDetail.html', {'materi': materi})
