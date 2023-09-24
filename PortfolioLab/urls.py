"""
URL configuration for PortfolioLab project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.views.generic import TemplateView

from PortfolioLab_app.views import (MainView, DonationView, LoginView, RegistrationView, logout_view,
                                    InstitutionCreateView, UserInfoView, CategoryCreateView, UserDonation, SuccessView,
                                    AllInstitutionView, InstitutionDeleteView, InstitutionUpdateView, UserUpdateView,
                                    DonationUpdateView, AllDonationView, EmailVerifyView, ResetPasswordSearchUserView,
                                    ResetPasswordView)

urlpatterns = [
    path('admin/', admin.site.urls  ),
    path('', MainView.as_view(), name='main'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('confirm_email/', TemplateView.as_view(template_name='confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/',EmailVerifyView.as_view(), name='verify_email'),
    path('invalid_verify/', TemplateView.as_view(template_name='invalid_verify.html'), name='invalid_verify'),
    path('reset_password/', ResetPasswordSearchUserView.as_view(), name='search_user'),
    path('reset_password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('userinfo/<int:user_id>/', UserInfoView.as_view(), name='profil'),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('donation/', DonationView.as_view(), name='donation'),
    path('all_donation/', AllDonationView.as_view(), name='all_donation'),
    path('my_donation/', UserDonation.as_view(), name='my_donation'),
    path('update_donation/<int:pk>/', DonationUpdateView.as_view(), name='update_donation'),
    path('institution/', AllInstitutionView.as_view(), name='all_institution'),
    path('add_institution/', InstitutionCreateView.as_view(), name='add_institution'),
    path('delete_institution/<int:pk>/', InstitutionDeleteView.as_view(), name='delete_institution'),
    path('update_institution/<int:pk>/', InstitutionUpdateView.as_view(), name='update_institution'),
    path('add_category/', CategoryCreateView.as_view()),
    path('success/', SuccessView.as_view(), name='success'),




]
