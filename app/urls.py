from django.urls import path
from app import views
from django.contrib.auth.views  import LoginView, LogoutView


urlpatterns = [
    path('',views.home_view, name='home-view'),
    path('adminclickview', views.admin_click_view, name='admin-click'),
    path('adminsignup', views.admin_signup_view, name='admin-signup'),

    path('afterlogin', views.after_login_view, name='after-login'),
    path('adminlogin', LoginView.as_view(template_name='itec/adminlogin.html'),name='adminlogin'),
    path('logout', LogoutView.as_view(template_name='itec/index.html')),
    path('admin-dashboard', views.admin_dashboard, name='admin-dashboard'),
    path('admin-trainer-view', views.admin_trainer_view, name='admin-trainer-view' ),
    path('admin-tambah-trainer', views.admin_tambah_trainer, name='admin-tambah-trainer'),

    path('admin-peserta-view', views.admin_peserta_view, name='admin-peserta-view'),
    path('admin-tambah-peserta', views.admin_tambah_peserta, name='admin-tambah-peserta'),

    path('list-pendaftar', views.admin_pendaftar_view, name='list-pendaftar'),
    path('admin-tambah-pendaftar/<int:id>', views.admin_tambah_pendaftar, name='admin-tambah-pendaftar'),

    path('admin-kelas-view', views.admin_kelas_view, name='admin-kelas-view'),
    path('admin-tambah-kelas',views.admin_tambah_kelas, name='admin-tambah-kelas'),

    path('admin-program-view', views.admin_program_view, name='admin-program-view'),
    path('tambah-program', views.admin_tambah_program, name='tambah-program'),
    path('edit-program/<int:id>', views.edit_program, name='edit-program'),
    path('hapus-program/<int:id>', views.hapus_progam, name='hapus-program'),


]