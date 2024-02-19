from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate


class UserRegistrationForm(forms.Form):
    """
    Formularz rejestracji użytkownika.
    """

    login = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_login(self):
        login = self.cleaned_data.get('login')

        if User.objects.filter(username=login).exists():
            raise ValidationError("Login jest już zajęty.")
        if not login:
            raise forms.ValidationError("To pole jest wymagane.")

        return login

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise ValidationError("Hasła nie są identyczne.")
        if not password and password_confirm:
            raise forms.ValidationError("To pole jest wymagane.")

class LoginForm(forms.Form):
    """
    Formularz logowania użytkownika.
    """

    login = forms.CharField(label="Login", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('login')
        password = cleaned_data.get('password')

        if not username or not password:
            raise forms.ValidationError("Wypełnij wszystkie pola.")

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Nieprawidłowy login lub hasło.")

class ShortenLinkForm(forms.Form):
    original_url = forms.URLField(label="URL", widget=forms.TextInput(attrs={'class': 'form-control'}))

    def save(self, user):
        original_url = self.cleaned_data['original_url']
        # Pobierz ostatni skrócony link użytkownika
        last_shortened_link = ShortenedLink.objects.filter(user=user).order_by('-id').first()
        last_id = 0
        if last_shortened_link:
            last_id = int(last_shortened_link.shortened_url.split('/')[-2])  # Pobierz ostatnią liczbę z ostatniego linku
        next_id = last_id + 1

        # Utwórz skrócony link dla nowego linku
        shortened_url = f'http://localhost:8000/{next_id}/'

        # Dodanie skróconego linku do bazy danych
        ShortenedLink.objects.create(user=user, original_url=original_url, shortened_url=shortened_url)