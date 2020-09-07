from django.contrib import admin
from app.models import Pendaftaran, Peserta, Trainer, Kelas, Program
# Register your models here.

class PesertaAdmin(admin.ModelAdmin):
    list_display = ('nama_peserta', 'alamat', 'nomor_handphone', 'pendidikan_terakhir',)

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('nama_program', 'biaya', 'keterangan')

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('nama_trainer', 'alamat', 'nomor_handphone', 'pendidikan_terakhir',)

class KelasAdmin(admin.ModelAdmin):
    list_display = ['nama_kelas', 'program',]

admin.site.register(Peserta, PesertaAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Pendaftaran)
admin.site.register(Kelas, KelasAdmin)

