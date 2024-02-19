from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .forms import LoginForm, UserRegistrationForm, ShortenLinkForm
from .models import ShortenedLink
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

class LoginFormView(View):
    # Widok logowania
    def get(self, request):
        # Tworzenie formularza logowania i przekazanie danych z żądania
        form = LoginForm()
        # Pobierz URL 'next' z parametru GET lub pusty ciąg znaków, jeśli nie istnieje
        next_url = request.GET.get('next', '')

        # Przekazujemy formularz i 'next' jako kontekst do szablonu
        return render(request, "login-form.html", {'form': form, 'next': next_url})

    def post(self, request):
        # Tworzenie formularza logowania i przekazanie danych z żądania
        form = LoginForm(request.POST)

        # Pobierz URL 'next' z parametru GET lub pusty ciąg znaków, jeśli nie istnieje
        next_url = request.GET.get('next', '')

        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)

                if next_url:
                    # Przekieruj na 'next', jeśli istnieje
                    return redirect(next_url)
                else:
                    # Przekieruj na domyślny widok, jeśli nie ma 'next'
                    return redirect('index')

        # Jeśli formularz jest nieprawidłowy lub autentykacja nie powiodła się, wyświetl stronę logowania
        return render(request, "login-form.html", {'form': form, 'next': next_url})

class LogoutView(View):
    # Widok wylogowywania
    def get(self, request):
        logout(request)
        f = LoginForm()
        return render(request, "login-form.html", {'form': f})

class Add_UserView(View):
    # Widok dodawania użytkownika
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Pobranie danych z formularza
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # Tworzenie nowego użytkownika
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

            # Komunikat o pomyślnym utworzeniu użytkownika
            messages.success(request, "Użytkownik został pomyślnie zarejestrowany.")
            # Przekierowanie na stronę logowania z komunikatem sukcesu
            return redirect('login')
        else:
            # Przekazanie formularza z błędami
            return render(request, 'register.html', {'form': form})

class IndexView(LoginRequiredMixin, View):
    login_url = '/login/'  # Adres URL do przekierowania, jeśli użytkownik nie jest zalogowany

    def get(self, request):
        form = ShortenLinkForm()
        shortened_links = ShortenedLink.objects.filter(user=request.user)
        return render(request, 'index.html', {'form': form, 'shortened_links': shortened_links})

    def post(self, request):
        form = ShortenLinkForm(request.POST)
        if form.is_valid():
            # Pobierz ostatni skrócony link użytkownika
            last_shortened_link = ShortenedLink.objects.filter(user=request.user).order_by('-id').first()
            last_id = 0
            if last_shortened_link:
                last_id = int(last_shortened_link.shortened_url.split('/')[-2])
            next_id = last_id + 1

            # Utwórz skrócony link dla nowego linku
            shortened_url = f'http://localhost:8000/{next_id}/'

            # Dodanie skróconego linku do bazy danych
            ShortenedLink.objects.create(user=request.user, original_url=form.cleaned_data['original_url'], shortened_url=shortened_url)
            return redirect('index')  # Przekierowanie na stronę główną
        else:
            shortened_links = ShortenedLink.objects.filter(user=request.user)
            return render(request, 'index.html', {'form': form, 'shortened_links': shortened_links})


class LinkDetailsView(LoginRequiredMixin, View):
    login_url = '/login/'  # Adres URL do przekierowania, jeśli użytkownik nie jest zalogowany

    def get(self, request, link_id):
        link = get_object_or_404(ShortenedLink, id=link_id)

        # Sprawdź, czy użytkownik jest właścicielem linku
        if link.user != request.user:
            return redirect('index')  # Przekieruj na stronę główną, jeśli link nie należy do użytkownika

        return render(request, 'link_details.html', {'link': link})

    def post(self, request, link_id):
        link = get_object_or_404(ShortenedLink, id=link_id)

        # Sprawdź, czy użytkownik jest właścicielem linku
        if link.user != request.user:
            return redirect('index')  # Przekieruj na stronę główną, jeśli link nie należy do użytkownika

        # Usunięcie linku
        link.delete()

        # Przekierowanie użytkownika na stronę główną
        return redirect('index')

class RedirectView(View):
    def get(self, request, link_id):
        try:
            link = ShortenedLink.objects.get(id=link_id)
            return redirect(link.original_url)
        except (ShortenedLink.DoesNotExist, ValueError):
            pass

        # Jeśli link nie istnieje lub podane ID jest nieprawidłowe, przekieruj na stronę główną
        return redirect('index')