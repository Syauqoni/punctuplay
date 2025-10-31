from django.shortcuts import render

# Create your views here.
def MateriDetail(request):
    return render(request, 'materi/MateriDetail.html')

def MateriMenuBelajar(request):
    return render(request, 'materi/MateriMenuBelajar.html')