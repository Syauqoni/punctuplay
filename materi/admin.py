from django.contrib import admin
from .models import Materi

@admin.register(Materi)
class MateriAdmin(admin.ModelAdmin):
    list_display = ('judul',)
