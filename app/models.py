from django.db import models
from django.contrib.auth.models import User

Kel = (
    ('Pria', 'Pria'),
    ('Wanita', 'Wanita'),
)

class Peserta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_peserta = models.CharField(max_length=100, null=False, blank=False)
    kelamin = models.CharField(choices=Kel, null=False, blank=False, max_length=50)
    tempat_lahir = models.CharField(max_length=100, blank=False, null=False)
    tgl_lahir = models.DateField(blank=True, null=True)
    nomor_handphone = models.CharField(max_length=12, null=False, blank=False, unique=True)
    agama = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=False, blank=False)
    sosmed = models.CharField(max_length=100, null=True, blank=True)
    pendidikan_terakhir = models.CharField(max_length=100, null=True, blank=True)
    alamat = models.CharField(max_length=100, null=False, blank=False)
    alasan_kursus = models.CharField(max_length=100, null=False, blank=False)
    is_peserta = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Form Peserta'
        verbose_name_plural = 'Data Peserta'

    def __str__(self):
        return self.nama_peserta

class Program(models.Model):
    nama_program = models.CharField(max_length=100, blank=False, null=False)
    biaya = models.DecimalField(max_digits=15, decimal_places=2)
    keterangan = models.TextField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.nama_program

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_trainer = models.CharField(max_length=100, null=False, blank=False)
    kelamin = models.CharField(choices=Kel, max_length=50, null=False, blank=False)
    tempat_lahir = models.CharField(max_length=50, null=True, blank=True)
    tgl_lahir = models.DateField(blank=True, null=True)
    nomor_handphone = models.CharField(max_length=12, null=False, blank=False, unique=True)
    agama = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=59, null=False, blank=False)
    sosmed = models.CharField(max_length=50, null=True, blank=True)
    pendidikan_terakhir = models.CharField(max_length=50, null=True, blank=True)
    alamat = models.CharField(max_length=50, null=True, blank=True)
    is_trainer = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Form Trainer'
        verbose_name_plural = "Data Trainer"
    
    def __str__(self):
        return self.nama_trainer

class Pendaftaran(models.Model):
    peserta = models.ForeignKey(Peserta, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    is_register = models.BooleanField(default=True) # True = belum punya kelas
    keterangan = models.TextField(max_length=100, blank=False, null=False)

class Kelas(models.Model):
    nama_kelas = models.CharField(max_length=50, null=False, blank=False)
    pendaftaran = models.ManyToManyField(Pendaftaran)
    program = models.ForeignKey(Program,  on_delete=models.SET_NULL, blank=True, null=True)
    trainer = models.ManyToManyField(Trainer)
    is_active = models.BooleanField(default=True)
    tgl_mulai = models.DateField(blank=True, null=True)
    tgl_berakhir = models.DateField(blank=True, null=True)
    keterangan = models.TextField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.nama_kelas
