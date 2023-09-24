from django import forms
from django.core.exceptions import ValidationError
from django.forms import TextInput, Select, SelectMultiple
import re
from django.contrib.auth.models import User

from .models import Donation, Institution, Category


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['quantity', 'categories', 'institution', 'address', 'phone_number', 'city', 'zip_code',
                  'pick_up_date', 'pick_up_time', 'pick_up_comment', 'user', ]


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'description', 'type', 'category']
        widgets = {
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nazwa',
            }),
            'description': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Opis'
            }),
            'type': Select(attrs={
                'class': 'form-control',
            }),
            'category': SelectMultiple(attrs={
                'class': 'form-control',
            })
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class RegistrationForm(forms.ModelForm):
    password_confirmation = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "Powtórz hasło"}))

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirmation', 'first_name', 'last_name')
        widgets = {

            'username': forms.EmailInput(attrs={
                'class': 'form-control',
                "placeholder": "Email"

            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                "placeholder": "Hasło"
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "imię"
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                "placeholder": "Nazwisko"
            })

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        email = self.cleaned_data.get('username')
        if User.objects.filter(username=email).exists():
            raise ValidationError('Ten email jest już używany.')

        if len(password) < 8:
            raise ValidationError ("Hasło musi zawierać co najmniej 8 znaków")

        if (not re.search(r'[a-z]', password) or
                not re.search(r'[A-Z]', password) or
                not re.search(r'\d', password) or
                not re.search(r'[!@#$%^&*()\-_=+[\]{};:\'",<.>/?\\|]', password)):
            raise ValidationError( "Hasło musi zawierać co najmniej jedną wielką literę, jedną małą literę, cyfrę i znak specjalny")

        if password and password_confirmation and password != password_confirmation:
            raise ValidationError('Hasła muszą buć takie same.')

        return cleaned_data


class LoginForm(forms.Form):
    login = forms.CharField(label='email', widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": "Email"}))

    password = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "Hasło"}))



class DonationUpdateForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['is_taken']
        labels = {
            'is_taken': 'Czy dar został odebrany?'
        }


class UserUpdateForm(forms.ModelForm):
    current_password = forms.CharField(widget=forms.PasswordInput, label='Obecne hasło', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło', required=False)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło', required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Email',
            'first_name': 'Imię',
            'last_name': 'Nazwiśko',
        }


class SearchUserForm(forms.Form):
    username = forms.CharField()

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label="Password confirmation", widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError('Podane hasła różnią się')

        if len(password) < 8:
            raise ValidationError("Hasło musi zawierać co najmniej 8 znaków")

        if (not re.search(r'[a-z]', password) or
                not re.search(r'[A-Z]', password) or
                not re.search(r'\d', password) or
                not re.search(r'[!@#$%^&*()\-_=+[\]{};:\'",<.>/?\\|]', password)):
            raise ValidationError( "Hasło musi zawierać co najmniej jedną wielką literę, jedną małą literę, cyfrę i znak specjalny")

        if password and password_confirmation and password != password_confirmation:
            raise ValidationError('Hasła muszą buć takie same.')

        return cleaned_data