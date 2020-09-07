from django.urls import path
from app import views, trainerView
from django.contrib.auth.views  import LoginView, LogoutView

urlpatterns = [
    path('trainer_click', views.trainer_click_view, name='trainer_click'),
    path('after-login', trainerView.after_login_view, name='after-login'),
    path('trainer-login', LoginView.as_view(template_name='itec/trainerlogin.html'), name='trainer-login'),
    path('trainer-signup', trainerView.trainer_signup, name='trainer-signup'),
    path('trainer-dashboard', trainerView.trainer_dashboard, name='trainer-dashboard'),
]