from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from main_app.models import Donation, Institution, Category
from main_app.forms import RegisterForm
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date, datetime
from main_app.functions import validate_password


class LandingPageView(View):
    def get(self, request):
        donations = Donation.objects.all()
        all_bags = 0
        for donation in donations:
            all_bags += donation.quantity
        institutions = Institution.objects.all()
        supported_institutions = 0
        for institution in institutions:
            institution_donations = institution.donation_set.all()
            if len(institution_donations) > 0:
                supported_institutions += 1
        foundations = Institution.objects.all().filter(type='foundation')
        organizations = Institution.objects.all().filter(type='non-governmental organization')
        local_collections = Institution.objects.all().filter(type='local collection')
        # pag_foundations = Paginator(foundations, 5)
        # pag_organizations = Paginator(organizations, 5)
        # pag_local_collections = Paginator(local_collections, 5)
        return render(request, 'index.html', {'all_bags': all_bags, 'supported_institutions': supported_institutions,
                                              'foundations': foundations, 'organizations': organizations,
                                              'local_collections': local_collections})


class AddDonationView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        return render(request, 'form.html', {'categories': categories, 'institutions': institutions})

    def post(self, request):
        donation = Donation.objects.create(
            quantity=request.POST.get('bags'),
            institution_id=request.POST.get('organization'),
            address=request.POST.get('address'),
            phone_number=request.POST.get('phone'),
            city=request.POST.get('city'),
            zip_code=request.POST.get('postcode'),
            pick_up_date=request.POST.get('data'),
            pick_up_time=request.POST.get('time'),
            pick_up_comment=request.POST.get('more_info'),
            user=request.user
        )
        categories = request.POST.getlist('categories')
        donation.categories.set(categories)
        return render(request, 'form-confirmation.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is None:
            messages.error(request, 'Błędny login lub hasło')
            return redirect('register')
        else:
            login(request, user)
            return redirect('main')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        first_name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('password2')
        val_pas = validate_password(pass1)
        has_error = False
        if val_pas is None:
            messages.error(request, 'Hasło musi mieć co najmniej 8 znaków, zawierać wielkie i małe litery, '
                                    'cyfry i znaki specjalne')
            has_error = True
        if pass1 != pass2:
            messages.error(request, 'Hasła muszą być takie same')
            has_error = True
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Podany email jest już zajęty')
            has_error = True
        if has_error:
            return render(request, 'register.html')
        else:
            User.objects.create_user(username=email, password=pass1, first_name=first_name, last_name=surname, email=email)
            messages.add_message(request, messages.SUCCESS, 'Pomyślnie utworzyłeś konto. Zaloguj się poniżej')
            return redirect('login')


class ProfileInfoView(View):
    def get(self, request):
        donations = Donation.objects.all().filter(user=request.user).order_by('pick_up_date').order_by('is_taken')
        return render(request, 'profileinfo.html', {'donations': donations})

    def post(self, request):
        don_id = request.POST.get('donation_id')
        don = Donation.objects.get(id=don_id)
        don.is_taken = True
        don.pick_up_date = date.today()
        don.pick_up_time = datetime.now().strftime("%H:%M")
        don.save()
        return redirect('profile')


class ProfileEditView(View):
    def get(self, request):
        return render(request, 'profile_edit.html')

    def post(self, request):
        user = authenticate(username=request.user.username, password=request.POST.get('password'))
        if user is None:
            messages.error(request, 'Błędne hasło')
            return render(request, 'profile_edit.html')
        else:
            user.first_name = request.POST.get('name')
            user.last_name = request.POST.get('surname')
            user.email = request.POST.get('email')
            user.username = request.POST.get('email')
            user.save()
            return redirect('profile')


class PasswordChangeView(View):
    def post(self, request):
        user = authenticate(username=request.user.username, password=request.POST.get('old_password'))
        if user is None:
            messages.error(request, 'Błędne hasło')
            return redirect('profile-edit')
        else:
            pass1 = request.POST.get('new_password')
            pass2 = request.POST.get('new_password2')
            val_pas = validate_password(pass1)
            if val_pas is None:
                messages.error(request,
                               'Hasło musi mieć co najmniej 8 znaków, zawierać wielkie i małe litery, '
                               'cyfry i znaki specjalne')
                return redirect('profile-edit')
            if pass1 == pass2:
                user.set_password(pass1)
                user.save()
                return redirect('login')
            else:
                messages.error(request, 'Hasła muszą być takie same')
                return redirect('profile-edit')
