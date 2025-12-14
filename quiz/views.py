from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Quiz, Soal, RiwayatKuis
from django.contrib.auth import logout
from accounts.models import UserProfile
from django.http import JsonResponse
from django.db.models import Sum
import json


def simpan_jawaban_ajax(request):
    if request.method == "POST":
        soal_id = request.POST.get("soal_id")
        jawaban = request.POST.get("jawaban", "")

        jawaban_user = request.session.get("jawaban_user", {})
        jawaban_user[soal_id] = jawaban
        request.session["jawaban_user"] = jawaban_user
        request.session.modified = True

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})

# Helper untuk menghindari error .strip()
def normalize_answer(ans):
    if isinstance(ans, list):
        return "".join(str(a).strip() for a in ans)
    if isinstance(ans, str):
        return ans.strip()
    return str(ans).strip()


def MenuKuis(request):

    # Bersihkan jawaban lama
    if "jawaban_user" in request.session:
        del request.session["jawaban_user"]


    if "timer_quiz" in request.session:
        del request.session["timer_quiz"]

    request.session["reset_timer"] = True

    # Ambil profile user
    profile = request.user.userprofile

    level = request.GET.get("level", "1")

    # Batasi level sesuai level user
    if int(level) > profile.level:
        level = str(profile.level)

    kuis_list = Quiz.objects.filter(level=level)

    return render(request, "quiz/MenuKuis.html", {
        "kuis_list": kuis_list,
        "level": level,
        "profile": profile,
        "reset_timer": True,
    })



def tampil_soal(request, quiz_id, nomor):

    quiz = get_object_or_404(Quiz, id=quiz_id)
    soal_list = quiz.soal.all().order_by("urutan")
    total = soal_list.count()

    if nomor == 0 and request.method == "GET" and "start" in request.GET:
        request.session["jawaban_user"] = {}
        request.session["sudah_mulai_quiz"] = True
        request.session.modified = True

    if nomor < 0:
        nomor = 0

    if nomor >= total:
        return redirect("hasil_jawaban", quiz_id=quiz_id)

    soal = soal_list[nomor]
    progress = int(((nomor + 1) / total) * 100)

    prev_nomor = nomor - 1 if nomor > 0 else None
    next_nomor = nomor + 1 if nomor + 1 < total else None

    jawaban_user = request.session.get("jawaban_user", {})
    jawaban_sebelumnya = jawaban_user.get(str(soal.id), "")

    # SIMPAN JAWABAN
    if request.method == "POST":

        if soal.tipe == "isian":
            gabungan = []
            for i in range(1, 20):
                val = request.POST.get(f"isian{i}")
                if val is not None:
                    gabungan.append(val)
            jawaban = "".join(gabungan)

        else:
            jawaban = request.POST.get("jawaban", "")

        jawaban_user[str(soal.id)] = jawaban
        request.session["jawaban_user"] = jawaban_user
        request.session.modified = True

        if request.POST.get("timeout") == "1":
            request.session["sudah_mulai_quiz"] = False
            return redirect("hasil_jawaban", quiz_id=quiz_id)

        if nomor + 1 < total:
            return redirect("tampil_soal", quiz_id=quiz_id, nomor=nomor + 1)
        else:
            request.session["sudah_mulai_quiz"] = False
            return redirect("hasil_jawaban", quiz_id=quiz_id)

    TEMPLATE_MAP = {
        "pilgan": "quiz/Pilgan.html",
        "dragdrop": "quiz/DragandDrop.html",
        "isian": "quiz/Isian.html",
        "benarsalah": "quiz/BenarSalah.html",
    }

    template = TEMPLATE_MAP.get(soal.tipe, "quiz/Pilgan.html")

    context = {
        "quiz": quiz,
        "quiz_id": quiz_id,
        "soal": soal,
        "nomor": nomor,
        "total_soal": total,
        "progress": progress,
        "prev_nomor": prev_nomor,
        "next_nomor": next_nomor,
        "jawaban_sebelumnya": jawaban_sebelumnya,
    }

    if soal.tipe == "dragdrop":
        context["html_pertanyaan"] = soal.pertanyaan.replace("___", "<span class='drop-slot'></span>")
        context["drag_items"] = soal.jawaban_drag or []

    if soal.tipe == "isian":
        context["parts"] = soal.pertanyaan.split("___")

    return render(request, template, context)





# HASIL JAWABAN 
def HasilJawaban(request, quiz_id):

    quiz = get_object_or_404(Quiz, id=quiz_id)
    jawaban_user = request.session.get("jawaban_user", {})
    total_poin = 0

    data_pilgan = []
    data_drag = []
    data_bs = []
    data_isian = []

    semua_soal = Soal.objects.filter(id__in=jawaban_user.keys()).order_by("urutan")

    for s in semua_soal:

        user_raw = jawaban_user.get(str(s.id), "")
        user_ans = normalize_answer(user_raw)
        benar = False

        # 1. PILIHAN GANDA
        if s.tipe == "pilgan":

            kunci = normalize_answer(s.jawaban_benar)

            if user_ans == kunci:
                benar = True
                total_poin += s.poin

            data_pilgan.append({
                "pertanyaan": s.pertanyaan,
                "jawaban_user": user_ans,
                "jawaban_benar": kunci,
                "status": "Benar" if benar else "Salah",
                "penjelasan": s.penjelasan,
            })

        # 2. DRAG & DROP
        elif s.tipe == "dragdrop":

            raw_kunci = s.jawaban_benar
            if isinstance(raw_kunci, str):
                try:
                    kunci = json.loads(raw_kunci)
                except json.JSONDecodeError:
                    kunci = []
            else:
                kunci = raw_kunci

            # user jawaban selalu string dan diubah ke list
            user_list = [u.strip() for u in user_raw.split(",")] if isinstance(user_raw, str) else user_raw

            if user_list == kunci:
                benar = True
                total_poin += s.poin

            data_drag.append({
                "pertanyaan": s.pertanyaan,
                "urutan_user": user_list,
                "urutan_benar": kunci,
                "status": "Benar" if benar else "Salah",
                "penjelasan": s.penjelasan,
            })

        # ======================================
        # 3. BENAR / SALAH
        # ======================================
        elif s.tipe == "benarsalah":

            # user_raw tetap "1" / "0"
            user_ans = user_raw  

            # kunci juga disamakan ke "1" / "0"
            kunci = "1" if s.jawaban_benarsalah else "0"

            if user_ans == kunci:
                benar = True
                total_poin += s.poin

            data_bs.append({
                "pertanyaan": s.pertanyaan,
                "jawaban_user": "Benar" if user_ans == "1" else "Salah" if user_ans == "0" else "Tidak dijawab",
                "jawaban_benar": "Benar" if kunci == "1" else "Salah",
                "status": "Benar" if benar else "Salah",
                "penjelasan": s.penjelasan,
            })


        # 4. ISIAN
        elif s.tipe == "isian":

            kunci = normalize_answer(s.jawaban_isian)

            if user_ans == kunci:
                benar = True
                total_poin += s.poin

            data_isian.append({
                "pertanyaan": s.pertanyaan,
                "jawaban_user": user_ans if user_ans else "Tidak dijawab",
                "jawaban_isian": kunci,
                "status": "Benar" if benar else "Salah",
                "penjelasan": s.penjelasan,
            })


    riwayat, created = RiwayatKuis.objects.get_or_create(
    user=request.user,
    quiz=quiz,
)
    
    skor_lama = riwayat.skor

    # Update skor tertinggi
    if total_poin > riwayat.skor:
        riwayat.skor = total_poin
        riwayat.save()

    profile = request.user.userprofile

    # === AMBIL TIMER DARI SESSION ===
    timer = request.session.get("timer_quiz")

    if timer:
        try:
            waktu = float(timer)
            if riwayat.best_time is None or waktu < riwayat.best_time:
                riwayat.best_time = waktu
                riwayat.save()
        except ValueError:
            pass

    total_waktu = RiwayatKuis.objects.filter(
        user=request.user,
        best_time__isnull=False
    ).aggregate(Sum("best_time"))["best_time__sum"] or 0

            
    if created:
        poin_ditambahkan = total_poin
    else:
        poin_ditambahkan = total_poin - skor_lama
        if poin_ditambahkan < 0:
            poin_ditambahkan = 0

    profile.total_time_spent = total_waktu
    profile.total_poin += poin_ditambahkan
    profile.add_xp(poin_ditambahkan)
    profile.update_rank()
    profile.save()

    # Bersihkan session
    request.session.pop("timer_quiz", None)

    return render(request, "quiz/HasilJawaban.html", {
        "total_poin": total_poin,
        "pilgan": data_pilgan,
        "drag": data_drag,
        "benar_salah": data_bs,
        "isian": data_isian,
    })


def simpan_timer_ajax(request):
    if request.method == "POST":
        timer = request.POST.get("timer")
        request.session["timer_quiz"] = float(timer)
        request.session.modified = True
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})


def logout_user(request):
    logout(request)
    return redirect('index')
