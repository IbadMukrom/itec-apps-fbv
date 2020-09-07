from django.shortcuts import render, redirect, reverse
from .forms import FormPeserta, KelasForm, Pendaftaran, TrainerForm, AdminSignup, TambahPendaftaranForm, ProgramForm
from .models import Peserta, Program, Pendaftaran, Kelas, Trainer
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from itec.lib import useracak
from django.db import transaction

def home_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'itec/index.html')

def admin_click_view(request):
    if request.user.is_authenticated:
        return redirect('afterlogin')
    return render(request, 'itec/adminclickview.html')

def trainer_click_view(request):
    if request.user.is_authenticated:
        return render('afterlogin')
    return render(request, 'itec/trainerclickview.html')

def peserta_click_view(request):
    if request.user.is_authenticated:
        return render('afterlogin')
    return render(request, 'itec/pesertaclickview.html')

# signup related
@transaction.atomic
def admin_signup_view(request):
    form = AdminSignup()
    if request.method =='POST':
        form = AdminSignup(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            admin_group = Group.objects.get_or_create(name='admin')
            admin_group[0].user_set.add(user)
            return redirect('adminlogin')
    return render(request, 'itec/adminsignup.html', {'form':form})


def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_peserta(user):
    return user.groups.filter(name='peserta').exists()
def is_trainer(user):
    return user.groups.filter(name='trainer').exists()
    
def after_login_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_trainer(request.user):
        return redirect('trainer-dashboard')
    elif is_peserta(request.user):
        return redirect('peserta-dashboard')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard(request):
    pesertas = Peserta.objects.all().count()
    trainers = Trainer.objects.all().count()
    pendaftarans = Pendaftaran.objects.all().count()
    kelas = Kelas.objects.all().count()
    programs = Program.objects.all().count()
    data = {'pesertas': pesertas,
            'trainers': trainers, 
            'pendaftarans': pendaftarans, 
            'kelas': kelas, 
            'programs': programs
        }
    return render(request, 'itec/admin_dashboard.html', data)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_trainer_view(request):
    trainers = Trainer.objects.all()
    return render(request, 'itec/admin_trainer_view.html', {'trainers': trainers})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
@transaction.atomic
def admin_tambah_trainer(request):
    form = TrainerForm()
    if request.method == 'POST':
        form = TrainerForm(request.POST or None)
        if form.is_valid():
            trainer = form.save(commit=False)
            user = User()
            user.username = useracak()
            user.set_password('default')
            user.is_staff = True
            user.save()
            trainer.user = user
            trainer.save()
            print(trainer)

            trainer_group = Group.objects.get_or_create(name='trainer')
            trainer_group[0].user_set.add(user)
            return redirect('admin-trainer-view')
    return render(request, 'itec/admin_tambah_trainer.html', {'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_peserta_view(request):
    pesertas = Peserta.objects.all()
    return render(request, 'itec/admin_peserta_view.html', {'pesertas':pesertas})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_tambah_peserta(request):
    form = FormPeserta()
    if request.method == 'POST':
        form = FormPeserta(request.POST or None)
        if form.is_valid():
            peserta = form.save(commit=False)
            user = User()
            user.username = useracak()
            user.set_password('itec')
            user.is_staff = True
            user.save()
            peserta.user = user
            peserta.save()
            
            pendaftaran = Pendaftaran()
            pendaftaran.peserta = peserta
            pendaftaran.program = Program.objects.get(id=request.POST['program'])
            pendaftaran.keterangan = request.POST['keterangan']
            pendaftaran.save()

            peserta_group = Group.objects.get_or_create(name='peserta')
            peserta_group[0].user_set.add(user)
            return redirect('admin-peserta-view')
    return render(request, 'itec/admin_tambah_peserta.html', {'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_pendaftar_view(request):
    pendaftarans = Pendaftaran.objects.filter(is_register=True)
    return render(request, 'itec/list_pendaftar.html', {'pendaftarans':pendaftarans})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
@transaction.atomic
def admin_tambah_pendaftar(request, id):
    form = TambahPendaftaranForm()
    if request.method == 'POST':
        form = TambahPendaftaranForm(request.POST)
        if form.is_valid():
            peserta = Peserta.objects.get(id=id)
            program = Program.objects.get(id=int(request.POST['program']))
            pendaftaran = Pendaftaran()
            pendaftaran.peserta = peserta
            pendaftaran.program = program
            pendaftaran.keterangan = request.POST['keterangan']
            pendaftaran.save()
            
            return redirect('list-pendaftar')
    return render(request, 'itec/tambah_pendaftar.html', {'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_kelas_view(request):
    kelas = Kelas.objects.all()
    return render(request, 'itec/admin_kelas_view.html', {'kelas':kelas})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_tambah_kelas(request):
    form = KelasForm()
    if request.method == 'POST':
        form = KelasForm(request.POST)
        if form.is_valid():
            kelas = form.save()
            trainers = form.cleaned_data["trainer"]
            pendaftarans = form.cleaned_data["pendaftaran"]
            
            kelas.trainer.add(*list(trainers))
            
            for p in pendaftarans:
                p.is_register = False
                p.save()
                kelas.pendaftaran.add(p)

            return redirect('admin-kelas-view')
    return render(request, 'itec/admin_tambah_kelas.html', {'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_program_view(request):
    programs = Program.objects.all()
    return render(request, 'itec/admin_program_view.html', {'programs': programs})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_tambah_program(request):
    form = ProgramForm()
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin-program-view')
    return render(request, 'itec/tambah_program.html', {'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_program(request, id):
    program = Program.objects.get(id=id)
    form = ProgramForm(instance=program)
    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('admin-program-view')
    return render(request, 'itec/tambah_program.html', {'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def hapus_progam(request, id):
    progam = Program.objects.get(id=id)
    progam.delete()
    return redirect('admin-program-view')