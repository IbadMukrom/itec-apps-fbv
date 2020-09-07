from django.urls import path
from app import views, pesertaView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('peserta_click', pesertaView.peserta_click_view, name='peserta_click'),
    path('peserta-signup', pesertaView.peserta_signup, name='peserta-signup'),
    path('peserta-login', LoginView.as_view(template_name='itec/pesertalogin.html'), name='peserta-login'),
    path('after-login', pesertaView.after_login_view, name='after-login'),
    path('peserta-dashboard', pesertaView.peserta_dashboard, name='peserta-dashboard'),
    path('peserta-program', pesertaView.lihat_program, name='lihat-program'),
]