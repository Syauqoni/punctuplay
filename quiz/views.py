from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Quiz, Soal
from django.contrib.auth import logout

def MenuKuis(request):
    level = request.GET.get("level", "1")
    kuis_list = Quiz.objects.filter(level=level)

    return render(request, "quiz/MenuKuis.html", {
        "kuis_list": kuis_list,
        "level": level,
    })


def tampil_soal(request, quiz_id, nomor):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Ambil semua soal sesuai urutan
    soal_list = quiz.soal.all().order_by("urutan")
    total = soal_list.count()

    # Validasi nomor
    if nomor < 0 or nomor >= total:
        return redirect("hasil_jawaban")

    soal = soal_list[nomor]

    progress = int(((nomor + 1) / total) * 100)

    # Mapping tipe soal ke template yang Anda inginkan
    TEMPLATE_MAP = {
        "pilgan": "quiz/Pilgan.html",
        "dragdrop": "quiz/DragandDrop.html",
        "isian": "quiz/Isian.html",
        "benarsalah": "quiz/BenarSalah.html",
    }

    template = TEMPLATE_MAP.get(soal.tipe, "quiz/Pilgan.html")

    # Next URL
    if nomor + 1 < total:
        next_url = reverse("tampil_soal", args=[quiz_id, nomor + 1])
    else:
        next_url = reverse("hasil_jawaban")

    # ============================================================
    # DRAG & DROP
    # ============================================================
    if soal.tipe == "dragdrop":
        html_pertanyaan = soal.pertanyaan.replace(
            "___", "<span class='drop-slot'></span>"
        )

        drag_items = soal.jawaban_drag if soal.jawaban_drag else []

        return render(request, template, {
            "quiz": quiz,
            "soal": soal,
            "nomor": nomor,
            "total_soal": total,
            "progress": progress,
            "next_url": next_url,
            "html_pertanyaan": html_pertanyaan,
            "drag_items": drag_items,
        })

    # ISIAN 
    if soal.tipe == "isian":

        parts = soal.pertanyaan.split("___") 

        return render(request, template, {
            "quiz": quiz,
            "soal": soal,
            "nomor": nomor,
            "total_soal": total,
            "progress": progress,
            "next_url": next_url,
            "parts": parts,   
        })

    # ============================================================
    # PILGAN / BENAR-SALAH
    # ============================================================
    return render(request, template, {
        "quiz": quiz,
        "soal": soal,
        "nomor": nomor,
        "total_soal": total,
        "progress": progress,
        "next_url": next_url,
    })


def HasilJawaban(request):
    return render(request, 'quiz/HasilJawaban.html')


def logout_user(request):
    logout(request)
    return redirect('index')
