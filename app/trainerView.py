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


@transaction.atomic
def trainer_signup(request):
    form = TrainerForm()
    if request.method == 'POST':
        form = TrainerForm(request.POST)
        if form.is_valid():
            trainer = form.save(commit=False)
            user = User()
            user.username = useracak()
            user.is_staff = True
            user.set_password('itec') 
            user.save()
            trainer.user = user
            trainer.save()  

            trainer_group = Group.objects.get_or_create(name='trainer')
            trainer_group[0].user_set.add(user)
            return redirect('trainer_click')
    return render(request, 'itec/trainer_signup.html', {'form':form}) 

@login_required(login_url='trainer-login')
@user_passes_test(is_trainer)
def trainer_dashboard(request):
    kelas = Kelas.objects.filter(trainer=request.user.trainer.id)
    trainer = Trainer.objects.get(user_id=request.user.id)
    return render(request, 'itec/trainer_dashboard.html', {'kelas':kelas, 'trainer':trainer})

