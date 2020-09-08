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

def after_login_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_trainer(request.user):
        return redirect('trainer-dashboard')
    elif is_peserta(request.user):
        return redirect('peserta-dashboard')

def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_peserta(user):
    return user.groups.filter(name='peserta').exists()
def is_trainer(user):
    return user.groups.filter(name='trainer').exists()

@transaction.atomic
def peserta_signup(request):
    form = FormPeserta()
    if request.method == 'POST':
        form = FormPeserta(request.POST)
        if form.is_valid():
            peserta = form.save(commit=False)
            user = User()
            user.username = useracak()
            user.is_staff = True
            user.set_password('itec')
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
            return redirect('peserta_click')
    return render (request, 'itec/peserta_signup.html',{'form':form})

@login_required(login_url='peserta-lgoin')
@user_passes_test(is_peserta)
def peserta_dashboard(request):    
    data = {
        'kelas':Kelas.objects.all().filter(pendaftaran__peserta=request.user.peserta.id),
        'peserta':Peserta.objects.get(user_id=request.user.id),
    }
    return render(request,'itec/peserta_dashboard.html', context=data)

@login_required(login_url='peserta-lgoin')
@user_passes_test(is_peserta)
def lihat_program(request):
    progam = Program.objects.all()
    return render (request, 'itec/peserta_program.html', {'program':progam})