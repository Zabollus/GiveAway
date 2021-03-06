"""GiveAway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_app.views import LandingPageView, AddDonationView, LoginView, LogoutView, RegisterView, ProfileInfoView, \
    ProfileEditView, PasswordChangeView, ActivateView, ResetPassword, NewPasswordView, ContactMessageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='main'),
    path('add-donation/', AddDonationView.as_view(), name='add-donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileInfoView.as_view(), name='profile'),
    path('profile-edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('activate/<uid64>/<token>', ActivateView.as_view(), name='activate'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),
    path('new-password/<uid64>/<token>/', NewPasswordView.as_view(), name='new-password'),
    path('contact-message/', ContactMessageView.as_view(), name='contact-message')
]
