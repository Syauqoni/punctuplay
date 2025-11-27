from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Quiz, Soal, RiwayatKuis
from django.contrib.auth import logout
from accounts.models import UserProfile
from django.db.models import Sum
import json

# ============================================
# Helper untuk menghindari error .strip()
# ============================================
def normalize_answer(ans):
    if isinstance(ans, list):
        return "".join(str(a).strip() for a in ans)
    if isinstance(ans, str):
        return ans.strip()
    return str(ans).strip()


def MenuKuis(request):

    if "jawaban_user" in request.session:
        del request.session["jawaban_user"]

    level = request.GET.get("level", "1")
    kuis_list = Quiz.objects.filter(level=level)

    return render(request, "quiz/MenuKuis.html", {
        "kuis_list": kuis_list,
        "level": level,
    })


def tampil_soal(request, quiz_id, nomor):

    quiz = get_object_or_404(Quiz, id=quiz_id)
    soal_list = quiz.soal.all().order_by("urutan")
    total = soal_list.count()

        # 🟢 RESET JAWABAN JIKA MULAI KUIS BARU
    if nomor == 0:
        request.session["jawaban_user"] = {}

    if nomor < 0 or nomor >= total:
        return redirect("hasil_jawaban")

    soal = soal_list[nomor]
    progress = int(((nomor + 1) / total) * 100)

    # ========================
    # SIMPAN JAWABAN USER
    # ========================
    if request.method == "POST":

        # --- ISIAN ---
        if soal.tipe == "isian":
            gabungan = []
            for i in range(1, 20):
                val = request.POST.get(f"isian{i}")
                if val is not None:
                    gabungan.append(val)
            jawaban = "".join(gabungan)

        else:
            jawaban = request.POST.get("jawaban", "")

        jawaban_user = request.session.get("jawaban_user", {})
        jawaban_user[str(soal.id)] = jawaban
        request.session["jawaban_user"] = jawaban_user
        request.session.modified = True

        if nomor + 1 < total:
            return redirect("tampil_soal", quiz_id=quiz_id, nomor=nomor + 1)
        else:
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
        "soal": soal,
        "nomor": nomor,
        "total_soal": total,
        "progress": progress,
    }

    if soal.tipe == "dragdrop":
        context["html_pertanyaan"] = soal.pertanyaan.replace("___", "<span class='drop-slot'></span>")
        context["drag_items"] = soal.jawaban_drag or []

    if soal.tipe == "isian":
        context["parts"] = soal.pertanyaan.split("___")

    return render(request, template, context)


# ============================================
# HASIL JAWABAN (FINAL FIX)
# ============================================
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

        # ======================================
        # 1. PILIHAN GANDA
        # ======================================
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

        # ======================================
        # 2. DRAG & DROP
        # ======================================
        elif s.tipe == "dragdrop":

            raw_kunci = s.jawaban_benar
            if isinstance(raw_kunci, str):
                try:
                    kunci = json.loads(raw_kunci)
                except json.JSONDecodeError:
                    kunci = []
            else:
                kunci = raw_kunci

            # user jawaban selalu string → ubah ke list
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


        # ======================================
        # 4. ISIAN
        # ======================================
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

    selisih_poin = total_poin - riwayat.skor
    
    if total_poin > riwayat.skor:
        riwayat.skor = total_poin
        riwayat.save()

    # total_poin_leaderboard = RiwayatKuis.objects.filter(user=request.user).aggregate(Sum('skor'))['skor__sum'] or 0

    profile = UserProfile.objects.get(user=request.user)

    if selisih_poin > 0:
        profile.add_xp(selisih_poin)
        # profile.total_poin = total_poin_leaderboard
        # profile.add_poin(total_poin_leaderboard - profile.total_poin)
        profile.add_poin(selisih_poin)
        profile.update_rank()

        # while profile.xp >= profile.max_xp and profile.level < 15000:
        #     profile.xp -= profile.max_xp
        #     profile.level += 1
        #     profile.max_xp += 300  # max XP meningkat tiap full
        #     if profile.level > 15000:
        #         profile.level = 15000
        #         profile.xp = profile.max_xp
        #         break

    # profile.total_poin = total_poin_leaderboard
    profile.save()

    return render(request, "quiz/HasilJawaban.html", {
        "total_poin": total_poin,
        "pilgan": data_pilgan,
        "drag": data_drag,
        "benar_salah": data_bs,
        "isian": data_isian,
    })

def logout_user(request):
    logout(request)
    return redirect('index')
