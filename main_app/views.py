from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from main_app.models import Donation, Institution, Category
from main_app.forms import RegisterForm
from django.core.paginator import Paginator
from django.contrib import messages
from datetime import date, datetime
from main_app.functions import validate_password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage


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
            user = User.objects.create_user(username=email, password=pass1, first_name=first_name, last_name=surname,
                                            email=email, is_active=False)
            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string('activate.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            activation_email = EmailMessage(
                email_subject,
                message,
                'giveaway@giveaway.com',
                [email]
            )
            activation_email.send()
            messages.add_message(request, messages.SUCCESS, 'Pomyślnie utworzyłeś konto. Aby je aktywować wejdź w link '
                                                            'wysłany na Twój adres e-mail.')
            return redirect('login')


class ActivateView(View):
    def get(self, request, uid64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Konto aktywowane pomyślnie')
            return redirect('login')
        return render(request, 'activate_failed.html', status=401)


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


class ResetPassword(View):
    def get(self, request):
        return render(request, 'forgot_password.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(request, 'Konto z podanym adresem email nie istnieje.')
            return render(request, 'forgot_password.html')
        current_site = get_current_site(request)
        email_subject = 'Reset your password'
        message = render_to_string('reset_password_email.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': generate_token.make_token(user)
                                   })
        reset_password_email = EmailMessage(
            email_subject,
            message,
            'giveaway@giveaway.com',
            [email]
        )
        reset_password_email.send()
        return render(request, 'reset_password_confirmation.html')


class NewPasswordView(View):
    def get(self, request, uid64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            return render(request, 'reset_password.html')
        return render(request, 'activate_failed.html', status=401)

    def post(self, request, uid64, token):
        pass1 = request.POST.get('new_password')
        pass2 = request.POST.get('new_password2')
        val_pas = validate_password(pass1)
        if val_pas is None:
            messages.error(request,
                           'Hasło musi mieć co najmniej 8 znaków, zawierać wielkie i małe litery, '
                           'cyfry i znaki specjalne')
            return redirect('new-password', uid64=uid64, token=token)
        if pass1 == pass2:
            try:
                uid = force_str(urlsafe_base64_decode(uid64))
                user = User.objects.get(pk=uid)
            except Exception as identifier:
                user = None

            if user is not None and generate_token.check_token(user, token):
                user.set_password(pass1)
                user.save()
            return redirect('login')
        else:
            messages.error(request, 'Hasła muszą być takie same')
            return redirect('new-password', uid64=uid64, token=token)


class ContactMessageView(View):
    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        content = request.POST.get('message')
        email_subject = 'Wiadomość z formularza kontaktowego'
        message = render_to_string('contact_message.html',
                                   {
                                       'name': name,
                                       'surname': surname,
                                       'content': content,
                                   })
        admins = User.objects.all().filter(is_superuser=True)
        for admin in admins:
            contact_message_email = EmailMessage(
                email_subject,
                message,
                'giveaway@giveaway.com',
                [admin.email]
            )
            contact_message_email.send()
        return redirect('/')
